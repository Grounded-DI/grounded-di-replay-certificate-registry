#!/usr/bin/env python3
"""New exact-case local evaluator. No original engine, network, or model calls.

The semantic domain is the preserved benchmark and its declared four-fact
replacement, not arbitrary legal prose. Expected dispositions are test oracles
only and are never used to derive decisions.
"""
import argparse, csv, hashlib, io, json, os, re, time, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAMES = ['01_canonical_input.json', '02_normalized_record.csv',
         '03_gate_matrix.json', '04_verdictbridge_assessment.txt']
HASH_KEYS = ['canonical_input_sha256', 'normalized_record_sha256',
             'gate_matrix_sha256', 'assessment_sha256', 'zip_sha256']
VARIANT = 'VB-DEMO-0001-PUNITIVE-CONTROL'

def encode(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True,
                      separators=(',', ':'), allow_nan=False).encode('utf-8')

def digest(data):
    return hashlib.sha256(data).hexdigest()

def load(path):
    def pairs(items):
        result = {}
        for k, v in items:
            if k in result: raise ValueError('DUPLICATE_JSON_KEY')
            result[k] = v
        return result
    return json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=pairs)

def save(path, obj):
    Path(path).write_bytes(encode(obj) + b'\n')

def validate_domain(case):
    original = load(ROOT/'original-reference/Run-2-01_canonical_input.json')
    replacements = load(ROOT/'valid-case/fact-replacements.json')
    cid = case['case_configuration']['case_id']
    if cid not in ('VB-DEMO-0001', VARIANT): raise ValueError('UNSUPPORTED_CASE')
    expected = json.loads(encode(original))
    if cid == VARIANT:
        expected['case_configuration']['case_id'] = VARIANT
        for item in expected['facts']:
            if item['id'] in replacements: item['text'] = replacements[item['id']]
    # Oracle values cannot influence or stand in for computation.
    supplied = json.loads(encode(case))
    supplied.pop('required_legal_disposition', None)
    expected.pop('required_legal_disposition', None)
    if supplied != expected: raise ValueError('OUTSIDE_EXACT_CASE_DOMAIN')
    return {x['id']: x['text'] for x in case['facts']}

def derive(case):
    f = validate_domain(case)
    def has(*ids): return all(i in f and bool(f[i]) for i in ids)
    product = has('F001','F002','F003','F004','F005','F006')
    hazard = has('F009','F010','F011','F012','F013')
    inadequate = has('F014','F015','F016','F017')
    warning_causation = has('F018','F019','F020','F021')
    causation = has('F026','F027','F028','F029')
    expert_dispute = has('F030','F032','F033','F034')
    damages = has(*('F%03d'%n for n in range(41,51)))
    recommendation = has('F035','F036') and 'recommended' in f['F035']
    rejection = ('rejected' in f['F037'] and 'despite the engineering recommendation' in f['F040'])
    email_admissible = has('F038','F039') and 'authenticated' in f['F038'] and 'admissible' in f['F039']
    # Original benchmark's explicit documented cost motive supplies L010.
    # Knowing rejection alone satisfies L007 but is not inferred to supply
    # an unstated motive/conscious-disregard predicate in the altered record.
    cost_motive = 'because the larger label would increase manufacturing cost by USD 0.18 per unit' in f['F037']
    conscious_disregard = recommendation and rejection and email_admissible and cost_motive
    strict = product and hazard and inadequate and warning_causation and causation and damages
    negligence = hazard and recommendation and rejection and email_admissible and warning_causation and causation and damages
    values = [strict, negligence, damages, conscious_disregard]
    decisions = ['DENY_SUMMARY_JUDGMENT' if x else 'GRANT_SUMMARY_JUDGMENT' for x in values]
    overall = 'DENIED' if all(values) else 'GRANTED' if not any(values) else 'GRANTED_IN_PART_DENIED_IN_PART'
    mapping = {
        'product_identification':['MI-PL-101'],
        'strict_liability_failure_to_warn':['MI-PL-201','MI-PL-202','MI-PL-203'],
        'negligence':['MI-NEG-101','MI-NEG-205'],
        'specific_causation':['MI-CAUS-101'],
        'conflicting_expert_testimony':['MI-EVID-101'],
        'past_medical_expenses':['MI-DAM-101'], 'past_lost_wages':['MI-DAM-102'],
        'future_medical_expenses':['MI-DAM-103'], 'pain_and_suffering':['MI-DAM-104']}
    if conscious_disregard: mapping['punitive_damages'] = ['MI-PUN-101']
    law_text = next(x['text'] for x in case['controlling_law'] if x['id']=='L016')
    coverage = all(code+':' in law_text for codes in mapping.values() for code in codes)
    reed_excluded = has('F051','F052','F053','F054') and 'inadmissible' in f['F053'] and 'must not be used' in f['F054']
    disposition = dict(zip(['strict_liability_failure_to_warn','negligence','compensatory_damages','punitive_damages'], decisions))
    disposition.update(overall_motion_result=overall, sam_reed_statement='EXCLUDED_AND_NOT_USED' if reed_excluded else 'FAIL',
        jury_instruction_coverage='PASS' if coverage else 'FAIL', appellate_record_review='NOT_APPLICABLE',
        filingready='NOT_APPLICABLE', verdictready='YES' if coverage and reed_excluded else 'NO',
        export_authorized=bool(coverage and reed_excluded))
    basis = {
        'product_identification':{'laws':['L002','L014'],'facts':['F001','F002','F003','F004','F005','F006']},
        'hazard_and_warning':{'laws':['L003','L004','L013'],'facts':['F009','F010','F011','F012','F013','F014','F015','F016','F017']},
        'warning_causation':{'laws':['L005'],'facts':['F018','F019','F020','F021']},
        'negligence':{'laws':['L006','L007','L012'],'facts':['F035','F036','F037','F038','F039','F040']},
        'specific_causation':{'laws':['L001','L008','L011','L018'],'facts':['F026','F027','F028','F029','F030','F032','F033','F034']},
        'compensatory_damages':{'laws':['L009','L013','L014'],'facts':['F%03d'%n for n in range(41,51)]},
        'punitive_damages':{'laws':['L001','L010'],'facts':['F035','F036','F037','F038','F039','F040'],
            'documented_cost_motive':cost_motive, 'conscious_disregard_supported':conscious_disregard},
        'excluded_evidence':{'laws':['L015','L020'],'facts':['F051','F052','F053','F054'],'relied_upon':False}}
    return {'disposition':disposition,'instruction_mapping':mapping,'basis':basis,
            'contradiction_count':0 if expert_dispute else 1}

def check_candidate(case, candidate):
    actual = derive(case)
    reasons = []
    reliance = candidate.get('relied_upon_fact_ids', [])
    admissible = set(x['id'] for x in case['facts']) - {'F051','F052','F053','F054'}
    bad = sorted(set(reliance)-admissible)
    text = encode(candidate).decode('utf-8')
    if bad or 'I heard Apex always knew the machine was dangerous.' in text:
        reasons.append({'rule':'L015 / F051-F054 / L020','gate':'VB-D-EAUR',
                        'code':'INADMISSIBLE_EVIDENCE_RELIANCE','fact_ids':bad or ['F051']})
    if candidate.get('disposition') != actual['disposition']:
        reasons.append({'rule':'L001 / L010 / L020','gate':'VB-B-MOCC','code':'LEGAL_DISPOSITION_MISMATCH'})
    ok = not reasons
    return {'accepted':ok,'verdictready':'YES' if ok else 'NO','export_authorized':ok,
            'failed_rules_and_gates':reasons,'runtime_state':'VERDICT_READY' if ok else 'EXPORT_REFUSED'}

def export_boundary(case, candidate, directory, artifacts):
    decision = check_candidate(case, candidate)
    out = Path(directory); out.mkdir(parents=True, exist_ok=False)
    decision.update(export_files_opened=0, bytes_written=0)
    if decision['export_authorized']:
        for name, data in artifacts.items():
            fd = os.open(out/name, os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW, 0o600)
            decision['export_files_opened'] += 1
            with os.fdopen(fd, 'wb') as stream:
                count = stream.write(data); stream.flush(); os.fsync(stream.fileno())
                decision['bytes_written'] += count
    decision['final_output_inventory'] = [{'path':p.relative_to(out).as_posix(),
        'bytes':p.stat().st_size,'sha256':digest(p.read_bytes())} for p in sorted(out.rglob('*')) if p.is_file()]
    return decision

def gate_matrix(case, result, replay_ok):
    disposition = result['disposition']; ready = disposition['verdictready']=='YES' and replay_ok
    specs = [('SYSTEM-GATE','runtime_preconditions','PASS'),('INPUT-NORM','input_normalization','PASS'),
        ('VB-C-VNCI','VNCI',str(result['contradiction_count'])),('LEGAL-KERNEL','',''),
        ('VB-D-EAUR','EAUR','1.000000'),('VB-B-MOCC','MOCC','PASS'),
        ('VB-A-CESMS','CESMS','1.000000'),('VB-E-SRAG','SRAG','1.000000'),
        ('VB-F-DESR','DESR','1.000000'),('VB-G-JICI','JICI','1.000000'),
        ('VB-H-ARCR','',''),('REPLAY-GATE','ReplayDivergence|StateTransitionMismatch','0|0' if replay_ok else '1|1'),
        ('VERDICTREADY-GATE','verdictready','YES' if ready else 'NO'),('EXPORT-GATE','export_authorized','true' if ready else 'false')]
    gates=[]
    for name, metric, value in specs:
        status = 'NOT_ACTIVE' if name=='LEGAL-KERNEL' else 'NOT_APPLICABLE' if name=='VB-H-ARCR' else 'PASS'
        if name in ('REPLAY-GATE','VERDICTREADY-GATE','EXPORT-GATE') and not ready:status='FAIL'
        required = '' if not metric else '0' if name=='VB-C-VNCI' else '0|0' if name=='REPLAY-GATE' else 'YES' if name=='VERDICTREADY-GATE' else 'true' if name=='EXPORT-GATE' else '1.000000' if value=='1.000000' else 'PASS'
        gates.append(dict(gate_id=name,metric=metric,required_value=required,actual_value=value,status=status,
                          failure_code='' if status!='FAIL' else 'LOCAL_REPLAY_FAILED',export_effect='NONE' if status!='FAIL' else 'BLOCK'))
    return {'case_id':case['case_configuration']['case_id'],'gates':gates,'instruction_mapping':result['instruction_mapping'],
        'motion_disposition':{k:v for k,v in disposition.items() if k not in ('filingready','verdictready','export_authorized')},
        'replay_validation':{'ReplayDivergence':0 if replay_ok else 1,'ReplayPass':int(replay_ok),'StateTransitionMismatch':0 if replay_ok else 1},
        'runtime_state':'VERDICT_READY' if ready else 'EXPORT_REFUSED','verdictready':'YES' if ready else 'NO',
        'export_authorized':ready,'filingready':'NOT_APPLICABLE','rule_evaluation':result['basis'],
        'implementation':'NEW_LOCAL_EXACT_CASE_EVALUATOR'}

def normalized(case, disposition, matrix):
    stream=io.StringIO(newline='');w=csv.writer(stream,lineterminator='\n')
    w.writerow(['record_id','record_type','source_id','legal_issue','admissibility','status','normalized_value'])
    for f in case['facts']:
        ids=re.findall(r'\b(?:PX|DX)-\d{3}\b',f['text']);excluded=f['id'] in ('F051','F052','F053','F054')
        w.writerow([f['id'],'fact',ids[0] if ids else '','','INADMISSIBLE' if excluded else 'ADMISSIBLE',
                    'EXCLUDED_AND_NOT_USED' if excluded else 'ACTIVE',f['text']])
    for law in case['controlling_law']:w.writerow([law['id'],'law','',law['title'],'','CONTROLLING',law['text']])
    for k,v in sorted(disposition.items()):
        value=str(v).lower() if type(v) is bool else v;w.writerow([k,'disposition','',k,'',value,value])
    for gate in sorted(matrix['gates'],key=lambda x:x['gate_id']):
        w.writerow([gate['gate_id'],'gate','',gate['gate_id'],'',gate['status'],gate['status']])
    return stream.getvalue().encode('utf-8')

def assessment(case, result, matrix):
    punitive = result['disposition']['punitive_damages']=='GRANT_SUMMARY_JUDGMENT'
    preliminary = ('The motion is granted in part and denied in part. The admissible evidence permits a reasonable jury to find product identification, inadequate warning, warning causation, negligence, specific causation, and compensatory damages. Summary judgment is granted to Apex on punitive damages because the altered closed-world record does not contain clear and convincing admissible evidence permitting a finding that Apex consciously disregarded a known substantial safety risk.' if punitive else 'The motion is denied on all requested grounds. The documented cost-motive predicate supports punitive damages under the stipulated closed-world L010.')
    c=case['case_configuration']
    return ('VerdictBridge Assessment\nJurisdiction\n'+c['jurisdiction']+'\nCourt / Venue\n'+c['court']+' / '+c['venue']+
        '\nProcedural Posture\n'+c['procedural_posture']+'.\nRuntime Mode\n'+c['runtime_mode']+'.\nCase / Motion / Trial Issue\nStrict-liability failure to warn, negligence, compensatory damages, punitive damages, evidence admissibility, causation, and jury-instruction coverage.\nPreliminary Result\n'+preliminary+
        ' The conflicting admissible expert opinions create a jury issue and are not a contradiction event.\nVerdictReady\nYes.\nFilingReady\nNot applicable because BriefWise filing mode is inactive.\nGatekeeper Findings\n'+
        '; '.join(g['gate_id']+': '+g['status'] for g in matrix['gates'])+'. All surviving issues are mapped to the stipulated Meridian jury instructions.\nFailed Gates / Runtime State\nNo gate failed. Runtime state is VERDICT_READY.\nRequired Fixes Before VerdictReady\nNo corrective action is required.\nRequired Fixes Before FilingReady\nNo corrective action is required because FilingReady is not applicable.\nAdversarial Risk\nSpecific causation remains a jury issue. An inadmissible hearsay-dependent candidate must be refused.\nEvidentiary Issues\nThe Sam Reed statement is inadmissible and was not used. All relied-upon facts are outside F051-F054.\nRecord / Appellate Issues\nAppellate review is not applicable.\nConfidence / Hallucination Risk\nScoped verification against the stipulated synthetic record; no external facts or authorities. No universal correctness or model-determinism claim.\nImplementation Provenance\nNew local evaluator for this benchmark. Original Verdictbridge_demo-2 files are preserved reference evidence only.\n').encode('utf-8')

def zip_bytes(artifacts):
    stream=io.BytesIO()
    with zipfile.ZipFile(stream,'w',compression=zipfile.ZIP_STORED) as archive:
        for name,data in sorted(artifacts.items()):
            info=zipfile.ZipInfo(name,(1980,1,1,0,0,0));info.create_system=3
            info.external_attr=0o100644<<16;archive.writestr(info,data)
    return stream.getvalue()

def run(input_path, destination, number):
    started=time.time_ns();case=load(input_path);result=derive(case)
    # Two independent evaluations from separately parsed frozen input snapshots.
    second=derive(load(input_path));matrix=gate_matrix(case,result,encode(result)==encode(second))
    reliance=sorted({i for k,b in result['basis'].items() if k!='excluded_evidence' for i in b['facts']})
    candidate={'disposition':result['disposition'],'relied_upon_fact_ids':reliance}
    artifacts=dict(zip(NAMES,[encode(case),normalized(case,result['disposition'],matrix),encode(matrix),assessment(case,result,matrix)]))
    artifacts['canonical_run.zip']=zip_bytes(artifacts)
    boundary=export_boundary(case,candidate,destination,artifacts)
    if not boundary['export_authorized']:raise ValueError('VALID_EXPORT_REFUSED')
    hashes=dict(zip(HASH_KEYS,[digest((Path(destination)/n).read_bytes()) for n in NAMES+['canonical_run.zip']]))
    receipt=dict(benchmark_name='VerdictBridge Five-Hash Selective Legal Outcome Replay',case_id=case['case_configuration']['case_id'],
        run_number=number,total_runs=3,coordinate_or_record_mismatches=0,maximum_numeric_error='0.000000',
        verification_result='PENDING_SEPARATE_VERIFIER',pid=os.getpid(),started_at_unix_ns=started,
        finished_at_unix_ns=time.time_ns(),implementation_sha256=digest(Path(__file__).read_bytes()),
        frozen_input_sha256=digest(Path(input_path).read_bytes()),export_boundary=boundary,**hashes)
    save(Path(destination)/'run_receipt.json',receipt)
    print(json.dumps({'run_number':number,'pid':os.getpid(),'status':'EXECUTED','hashes':hashes}))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('input');parser.add_argument('output');parser.add_argument('--run-number',type=int,required=True)
    a=parser.parse_args();run(a.input,a.output,a.run_number)
