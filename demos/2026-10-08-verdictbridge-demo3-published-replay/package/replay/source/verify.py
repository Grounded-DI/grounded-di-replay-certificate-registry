#!/usr/bin/env python3
"""Separate verifier: no imports from evaluator or orchestration modules.

Checks the finite exact benchmark domain, not general legal interpretation.
Internal independent logic path, not external third-party certification.
"""
import argparse, csv, hashlib, io, json, re, sys, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REFERENCE_HASHES={
 'Run-2-01_canonical_input.json':'2e631eb0d2d81d6625ad73f286049ccc988dea8de31028880f774bf76a496042',
 'Run-2-02_normalized_record.csv':'0ccc7f002330baa8b482486fed0e17a1d73b4bd3c95372cc52bf172585ee1a97',
 'Run-2-03_gate_matrix.json':'3485237ad08fac0192e72873620b5207702687fd6efbb4d0949d6c0d5d2bd9a2',
 'Run-2-04_verdictbridge_assessment.txt':'e977081b390b42f74a6779a4ee32252afcd7aa58fb73def9d7181dda1163facd',
 'Run-2-run_receipt.json':'0882d41eef9dda1f9f097f609fce77edaf7629d508da34e6d0c532b312924044'}
REPLACEMENTS={
 'F037':'Apex marketing director Victor Hale rejected the proposed Zeta-9-specific warning recommended by Elena Cole. The record does not establish Hale’s reason for rejecting the proposed warning.',
 'F038':'Hale’s authenticated internal email is Record Exhibit PX-005.',
 'F039':'PX-005 is an admissible statement of a party opponent.',
 'F040':'PX-005 states that Apex would retain the shorter warning despite the engineering recommendation. PX-005 does not state that the decision was made to avoid a per-unit cost increase and does not state any other reason for the decision.'}
EXPECTED={'strict_liability_failure_to_warn':'DENY_SUMMARY_JUDGMENT','negligence':'DENY_SUMMARY_JUDGMENT',
 'compensatory_damages':'DENY_SUMMARY_JUDGMENT','punitive_damages':'GRANT_SUMMARY_JUDGMENT',
 'overall_motion_result':'GRANTED_IN_PART_DENIED_IN_PART','sam_reed_statement':'EXCLUDED_AND_NOT_USED',
 'jury_instruction_coverage':'PASS','appellate_record_review':'NOT_APPLICABLE','filingready':'NOT_APPLICABLE',
 'verdictready':'YES','export_authorized':True}
MAPPING={'product_identification':['MI-PL-101'],'strict_liability_failure_to_warn':['MI-PL-201','MI-PL-202','MI-PL-203'],
 'negligence':['MI-NEG-101','MI-NEG-205'],'specific_causation':['MI-CAUS-101'],
 'conflicting_expert_testimony':['MI-EVID-101'],'past_medical_expenses':['MI-DAM-101'],
 'past_lost_wages':['MI-DAM-102'],'future_medical_expenses':['MI-DAM-103'],'pain_and_suffering':['MI-DAM-104']}
FILES=['01_canonical_input.json','02_normalized_record.csv','03_gate_matrix.json','04_verdictbridge_assessment.txt','canonical_run.zip']
KEYS=['canonical_input_sha256','normalized_record_sha256','gate_matrix_sha256','assessment_sha256','zip_sha256']

def read(path): return json.loads(Path(path).read_text(encoding='utf-8'))
def hash_file(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def require(test, reason):
    if not test: raise ValueError(reason)

def check_case(root):
    for name,h in REFERENCE_HASHES.items():require(hash_file(root/'original-reference'/name)==h,'REFERENCE_CHANGED:'+name)
    original=read(root/'original-reference/Run-2-01_canonical_input.json')
    variant=read(root/'valid-case/01_canonical_input.json')
    expected=json.loads(json.dumps(original));expected['case_configuration']['case_id']='VB-DEMO-0001-PUNITIVE-CONTROL'
    for item in expected['facts']:
        if item['id'] in REPLACEMENTS:item['text']=REPLACEMENTS[item['id']]
    expected['required_legal_disposition']=EXPECTED
    require(variant==expected,'CANONICAL_VARIANT_NOT_EXACT')
    f={x['id']:x['text'] for x in variant['facts']};laws={x['id']:x['text'] for x in variant['controlling_law']}
    require(len(f)==58 and len(laws)==20,'FACT_OR_LAW_CARDINALITY')
    # Independent exact-record inference. Unchanged source facts establish
    # the liability/compensation elements; only the affirmative motive is gone.
    predicates={
        'product_identification':all(i in f for i in ['F001','F003','F004','F005','F006']),
        'foreseeable_hazard':'75 degrees' in f['F009'] and 'above 60' in f['F010'],
        'warning_inadequacy':'did not identify' in f['F015'] and 'did not require' in f['F016'] and 'did not require' in f['F017'],
        'warning_causation':'read and followed' in f['F020'] and 'would have used a respirator' in f['F021'],
        'negligent_breach':'recommended a Zeta-9-specific warning' in f['F035'] and 'rejected the proposed Zeta-9-specific warning' in f['F037'],
        'admissible_specific_causation':'substantial factor' in f['F027'] and 'admissible' in f['F029'],
        'compensation_supported':all(i in f for i in ['F041','F042','F044','F045','F047','F049']),
        'punitive_predicate_absent':'does not establish Hale’s reason' in f['F037'] and 'does not state that the decision was made to avoid a per-unit cost increase' in f['F040'],
        'reed_excluded':'inadmissible' in f['F053'] and 'must not be used' in f['F054'],
        'expert_conflict_not_contradiction':'factfinder' in f['F034'] and 'not a contradiction event' in laws['L018']}
    require(all(predicates.values()),'INDEPENDENT_PREDICATE_CHECK')
    require('USD 0.18' not in '\n'.join(f.values()),'AFFIRMATIVE_COST_PREDICATE_RETAINED')
    require('solely to avoid a per-unit cost increase' in laws['L010'],'L010_CHECK')
    require('No exception applies to Sam Reed' in laws['L015'] and 'all relied-upon evidence is admissible' in laws['L020'],'EXCLUSION_RULE_CHECK')
    for codes in MAPPING.values():
        for code in codes:require(code+':' in laws['L016'],'UNKNOWN_INSTRUCTION:'+code)
    return original,variant,predicates

def check_invalid_candidate(candidate):
    bad=sorted(set(candidate.get('relied_upon_fact_ids',[]))&{'F051','F052','F053','F054'})
    relies_on_reed=bool(bad) or 'I heard Apex always knew the machine was dangerous.' in json.dumps(candidate,ensure_ascii=False)
    require(relies_on_reed,'INVALID_CONTROL_NOT_HEARSAY_DEPENDENT')
    require(candidate['disposition']['punitive_damages']=='DENY_SUMMARY_JUDGMENT','INVALID_CONTROL_NOT_PUNITIVE_RESCUE')
    return {'status':'REFUSED','accepted':False,'verdictready':'NO','export_authorized':False,
        'failure_code':'INADMISSIBLE_EVIDENCE_RELIANCE','failed_rule':'L015 / F051-F054 / L020',
        'failed_gates':['VB-D-EAUR','VERDICTREADY-GATE','EXPORT-GATE'],'excluded_fact_ids':bad}

def check_run(root,folder,case,number):
    p=root/folder
    # Every run must reconstruct canonical bytes from the frozen JSON input.
    canonical=json.dumps(case,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode('utf-8')
    require((p/FILES[0]).read_bytes()==canonical,'RUN_CANONICAL_MISMATCH:'+folder)
    matrix=read(p/FILES[2]);d=dict(matrix['motion_disposition'],filingready=matrix['filingready'],verdictready=matrix['verdictready'],export_authorized=matrix['export_authorized'])
    require(d==EXPECTED,'OBSERVED_DISPOSITION_MISMATCH:'+folder)
    require(matrix['instruction_mapping']==MAPPING,'INSTRUCTION_MAPPING_MISMATCH:'+folder)
    require(matrix['runtime_state']=='VERDICT_READY','RUNTIME_STATE:'+folder)
    required=case['required_gate_results']['gates']
    require([(g['gate_id'],g['status']) for g in matrix['gates']]==[(g['gate_id'],g['status']) for g in required],'GATE_STATUS_MISMATCH:'+folder)
    for g in matrix['gates']:
        require(g['failure_code']=='' and g['export_effect']=='NONE','UNEXPECTED_GATE_FAILURE')
        require(g['actual_value']==g['required_value'],'GATE_VALUE_MISMATCH:'+g['gate_id'])
    require(matrix['replay_validation']=={'ReplayDivergence':0,'ReplayPass':1,'StateTransitionMismatch':0},'REPLAY_METRICS')
    basis=matrix['rule_evaluation'];require(basis['punitive_damages']['conscious_disregard_supported'] is False and basis['punitive_damages']['documented_cost_motive'] is False,'PUNITIVE_TRACE')
    require(basis['excluded_evidence']=={'laws':['L015','L020'],'facts':['F051','F052','F053','F054'],'relied_upon':False},'EXCLUSION_TRACE')
    facts={f['id']:f['text'] for f in case['facts']};laws={l['id']:l for l in case['controlling_law']}
    for name,item in basis.items():
        require(all(i in facts for i in item['facts']) and all(i in laws for i in item['laws']),'UNKNOWN_TRACE_ID')
        if name!='excluded_evidence':require(not set(item['facts'])&{'F051','F052','F053','F054'},'REED_USED_IN_TRACE')
    rows=list(csv.DictReader(io.StringIO((p/FILES[1]).read_text(encoding='utf-8'))))
    require(len(rows)==103,'NORMALIZED_ROW_COUNT')
    require(len({r['record_id'] for r in rows})==103,'DUPLICATE_NORMALIZED_ROWS')
    for row in rows:
        i=row['record_id'];kind=row['record_type']
        if kind=='fact':
            require(row['normalized_value']==facts[i],'CSV_FACT:'+i)
            excluded=i in ('F051','F052','F053','F054')
            require(row['admissibility']==('INADMISSIBLE' if excluded else 'ADMISSIBLE') and row['status']==('EXCLUDED_AND_NOT_USED' if excluded else 'ACTIVE'),'CSV_ADMISSIBILITY:'+i)
            ids=re.findall(r'\b(?:PX|DX)-\d{3}\b',facts[i]);require(row['source_id']==(ids[0] if ids else '') and row['legal_issue']=='','CSV_SOURCE:'+i)
        elif kind=='law':require(row['normalized_value']==laws[i]['text'] and row['legal_issue']==laws[i]['title'] and row['status']=='CONTROLLING','CSV_LAW:'+i)
        elif kind=='disposition':
            v=EXPECTED[i];v=str(v).lower() if type(v) is bool else v
            require(row['normalized_value']==v and row['status']==v,'CSV_DISPOSITION:'+i)
        elif kind=='gate':require(row['normalized_value']==next(g['status'] for g in matrix['gates'] if g['gate_id']==i),'CSV_GATE:'+i)
        else:raise ValueError('UNKNOWN_CSV_ROW')
    assessment=(p/FILES[3]).read_text(encoding='utf-8')
    for phrase in ['The motion is granted in part and denied in part.','Summary judgment is granted to Apex on punitive damages','does not contain clear and convincing admissible evidence','The Sam Reed statement is inadmissible and was not used.','VerdictReady\nYes.','not a contradiction event','New local evaluator for this benchmark.']:
        require(phrase in assessment,'ASSESSMENT_MISSING:'+phrase)
    hashes={k:hash_file(p/n) for k,n in zip(KEYS,FILES)}
    receipt=read(p/'run_receipt.json')
    require(all(receipt[k]==v for k,v in hashes.items()),'RECEIPT_HASH_MISMATCH')
    require(receipt['case_id']=='VB-DEMO-0001-PUNITIVE-CONTROL' and receipt['run_number']==number and receipt['total_runs']==3,'RECEIPT_ID')
    require(receipt['benchmark_name']=='VerdictBridge Five-Hash Selective Legal Outcome Replay','RECEIPT_BENCHMARK')
    require(receipt['coordinate_or_record_mismatches']==0 and receipt['maximum_numeric_error']=='0.000000','RECEIPT_ERROR_METRICS')
    require(receipt['implementation_sha256']==hash_file(root/'source/evaluator.py') and receipt['frozen_input_sha256']==hash_file(root/'valid-case/01_canonical_input.json'),'SOURCE_INPUT_BINDING')
    require(type(receipt['pid']) is int and receipt['finished_at_unix_ns']>=receipt['started_at_unix_ns'],'RUN_RECEIPT_TIME')
    boundary=receipt['export_boundary'];require(boundary['accepted'] and boundary['export_files_opened']==5 and boundary['bytes_written']==sum((p/n).stat().st_size for n in FILES),'VALID_BOUNDARY_RECORD')
    inventory=[{'path':n,'bytes':(p/n).stat().st_size,'sha256':hash_file(p/n)} for n in sorted(FILES)]
    require(boundary['final_output_inventory']==inventory,'VALID_EXPORT_INVENTORY')
    with zipfile.ZipFile(p/'canonical_run.zip') as z:
        require(z.namelist()==sorted(FILES[:4]) and z.testzip() is None,'ZIP_MEMBERS_OR_CRC')
        for info in z.infolist():
            require(z.read(info.filename)==(p/info.filename).read_bytes(),'ZIP_MEMBER_BYTES')
            require(info.date_time==(1980,1,1,0,0,0) and info.compress_type==zipfile.ZIP_STORED and info.external_attr==0o100644<<16 and info.create_system==3 and not info.extra and not info.comment,'ZIP_METADATA')
        require(not z.comment,'ZIP_COMMENT')
    return {'folder':folder,'hashes':hashes,'pid':receipt['pid'],'status':'PASS'}

def verify(root):
    root=Path(root);original,case,predicates=check_case(root)
    runs=[check_run(root,n,case,i) for i,n in enumerate(['Run-A','Run-B','Run-C'],1)]
    require(len({r['pid'] for r in runs})==3,'NOT_THREE_DISTINCT_PROCESSES')
    comparisons=[]
    for name,key in zip(FILES,KEYS):
        data=[(root/r['folder']/name).read_bytes() for r in runs]
        equal=data[0]==data[1]==data[2];hash_equal=len({r['hashes'][key] for r in runs})==1
        require(equal and hash_equal,'THREE_RUN_DIVERGENCE:'+name)
        comparisons.append({'artifact':name,'bytes':len(data[0]),'sha256':[r['hashes'][key] for r in runs],
            'direct_byte_comparison':'PASS','hash_comparison':'PASS','byte_mismatches':0})
    old=read(root/'original-reference/Run-2-03_gate_matrix.json')
    baseline=dict(old['motion_disposition'],filingready=old['filingready'],verdictready=old['verdictready'],export_authorized=old['export_authorized'])
    require(baseline==original['required_legal_disposition'],'ORIGINAL_EVIDENCE_DISAGREES')
    changed=[k for k in EXPECTED if baseline[k]!=EXPECTED[k]]
    require(set(changed)=={'punitive_damages','overall_motion_result'},'UNRELATED_OUTCOME_DRIFT')
    candidate=read(root/'invalid-hearsay-control/candidate-analysis.json');independent=check_invalid_candidate(candidate)
    stored=read(root/'invalid-hearsay-control/verifier-refusal.json')
    require(stored==independent,'STORED_VERIFIER_REFUSAL_MISMATCH')
    boundary=read(root/'invalid-hearsay-control/export-boundary-result.json')
    require(boundary['verdictready']=='NO' and boundary['export_authorized'] is False and boundary['accepted'] is False,'INVALID_CONTROL_ALLOWED')
    require(boundary['export_files_opened']==0 and boundary['bytes_written']==0 and boundary['final_output_inventory']==[],'INVALID_EXPORT_ACTIVITY')
    actual=[p.relative_to(root/'invalid-hearsay-control/exports').as_posix() for p in (root/'invalid-hearsay-control/exports').rglob('*') if p.is_file()]
    require(actual==[],'INVALID_EXPORT_PRESENT')
    require(read(root/'invalid-hearsay-control/export-open-audit.json')==[],'AUDITED_INVALID_EXPORT_OPEN')
    require(any(x['code']=='INADMISSIBLE_EVIDENCE_RELIANCE' for x in boundary['failed_rules_and_gates']),'REFUSAL_CODE_MISSING')
    return {'status':'PASS','case_id':'VB-DEMO-0001-PUNITIVE-CONTROL','reference_files_checked':5,
        'independent_predicate_checks':predicates,'observed_disposition':EXPECTED,'runs':runs,
        'three_run_five_hash_match':'PASS','direct_byte_comparison':comparisons,
        'selectivity':[{'field':k,'original':baseline[k],'new':EXPECTED[k],'changed':k in changed} for k in EXPECTED],
        'invalid_control':dict(independent,export_files_opened=0,bytes_written=0,final_output_inventory=[]),
        'maximum_numeric_error':'0.000000','numeric_error_scope':'No numeric damages values were changed; exact input/normalized-record preservation. Not a predictive error metric.',
        'limitations':['New exact-case local implementation; original engine not executed.','Separate verifier authored in the same task; no external certification.','No model calls or real-world legal authority validation.','Finite exact-case result; no universal model determinism.']}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--root',default=str(ROOT));parser.add_argument('--candidate');a=parser.parse_args()
    try:
        if a.candidate:
            check_case(Path(a.root));result=check_invalid_candidate(read(a.candidate));print(json.dumps(result,indent=2));sys.exit(2)
        print(json.dumps(verify(a.root),indent=2))
    except Exception as e:
        print(json.dumps({'status':'FAIL','reason':str(e)},indent=2));sys.exit(1)
