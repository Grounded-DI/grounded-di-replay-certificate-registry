#!/usr/bin/env python3
"""Meaningful controls on isolated copies; preserve original package bytes."""
import copy, importlib.util, json, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def acceptance():
    controls=[]
    for name in ['reference_law','restored_cost_fact','wrong_disposition','reed_in_trace','missing_export','forged_receipt','zip_byte_change']:
        with tempfile.TemporaryDirectory(prefix='vb-demo3-tamper-') as t:
            dest=Path(t)/'package';shutil.copytree(ROOT,dest)
            if name=='reference_law':
                p=dest/'original-reference/Run-2-01_canonical_input.json';obj=json.loads(p.read_text());obj['controlling_law'][9]['text']='Changed rule';p.write_text(json.dumps(obj))
            elif name=='restored_cost_fact':
                p=dest/'valid-case/01_canonical_input.json';obj=json.loads(p.read_text());obj['facts'][36]['text']='Hale rejected the warning solely to avoid USD 0.18 per unit.';p.write_text(json.dumps(obj))
            elif name in ('wrong_disposition','reed_in_trace'):
                p=dest/'Run-A/03_gate_matrix.json';obj=json.loads(p.read_text())
                if name=='wrong_disposition':obj['motion_disposition']['punitive_damages']='DENY_SUMMARY_JUDGMENT'
                else:obj['rule_evaluation']['punitive_damages']['facts'].append('F051')
                p.write_text(json.dumps(obj))
            elif name=='missing_export':(dest/'Run-A/04_verdictbridge_assessment.txt').unlink()
            elif name=='forged_receipt':
                p=dest/'Run-A/run_receipt.json';obj=json.loads(p.read_text());obj['zip_sha256']='0'*64;p.write_text(json.dumps(obj))
            else:
                p=dest/'Run-A/canonical_run.zip';data=bytearray(p.read_bytes());data[-1]^=1;p.write_bytes(data)
            proc=subprocess.run([sys.executable,'-B',str(dest/'source/verify.py')],capture_output=True,text=True)
            if proc.returncode==0:raise ValueError('ALTERED_COPY_ACCEPTED:'+name)
            controls.append({'test':name,'rejected':True,'verifier_exit_code':proc.returncode,'result':json.loads(proc.stdout)})
    spec=importlib.util.spec_from_file_location('local_eval',ROOT/'source/evaluator.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    original=module.load(ROOT/'original-reference/Run-2-01_canonical_input.json')
    baseline=module.derive(original)
    if baseline['disposition']!=original['required_legal_disposition']:raise ValueError('BASELINE_LOCAL_RECALCULATION_MISMATCH')
    case=module.load(ROOT/'valid-case/01_canonical_input.json');changed=copy.deepcopy(case)
    changed['required_legal_disposition']={'punitive_damages':'DENY_SUMMARY_JUDGMENT','export_authorized':False}
    if module.derive(case)!=module.derive(changed):raise ValueError('EVALUATOR_READS_ORACLE_AS_DECISION')
    with tempfile.TemporaryDirectory(prefix='vb-demo3-forged-') as t:
        forged={'disposition':dict(module.derive(case)['disposition'],punitive_damages='DENY_SUMMARY_JUDGMENT'),
                'relied_upon_fact_ids':['F035','F037']}
        refusal=module.export_boundary(case,forged,Path(t)/'exports',{'result.txt':b'wrong result'})
        if refusal['export_authorized'] or refusal['export_files_opened'] or refusal['bytes_written'] or refusal['final_output_inventory']:
            raise ValueError('WRONG_DISPOSITION_EXPORT_ALLOWED')
    return {'status':'PASS','tamper_controls':controls,'oracle_independence':'PASS',
        'baseline_local_recalculation':baseline['disposition'],
        'baseline_scope':'New evaluator recalculation against preserved reference outcomes; not original engine execution.',
        'wrong_disposition_export_refusal':refusal}

if __name__=='__main__':
    try:print(json.dumps(acceptance(),indent=2))
    except Exception as e:print(json.dumps({'status':'FAIL','reason':str(e)}));sys.exit(1)
