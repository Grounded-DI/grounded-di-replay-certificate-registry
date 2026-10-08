#!/usr/bin/env python3
"""Repeat the experiment in a new destination; never overwrite a release."""
import argparse, json, shutil, subprocess, sys
from pathlib import Path

def main():
    parser=argparse.ArgumentParser();parser.add_argument('destination');a=parser.parse_args()
    source=Path(__file__).resolve().parents[1];dest=Path(a.destination).resolve()
    if dest.exists():raise ValueError('DESTINATION_ALREADY_EXISTS')
    dest.mkdir(parents=True)
    for name in ['original-reference','valid-case','source']:shutil.copytree(source/name,dest/name)
    (dest/'verification').mkdir()
    for i,name in enumerate(['Run-A','Run-B','Run-C'],1):
        subprocess.run([sys.executable,'-B',str(dest/'source/evaluator.py'),str(dest/'valid-case/01_canonical_input.json'),str(dest/name),'--run-number',str(i)],check=True)
    subprocess.run([sys.executable,'-B',str(dest/'source/invalid_control.py'),str(dest/'invalid-hearsay-control')],check=True)
    p=subprocess.run([sys.executable,'-B',str(dest/'source/verify.py'),'--candidate',str(dest/'invalid-hearsay-control/candidate-analysis.json')],capture_output=True,text=True)
    (dest/'invalid-hearsay-control/verifier-refusal.json').write_text(p.stdout)
    (dest/'invalid-hearsay-control/verifier-exit-code.txt').write_text(str(p.returncode)+'\n')
    if p.returncode!=2:raise ValueError('INVALID_CONTROL_NOT_REFUSED')
    p=subprocess.run([sys.executable,'-B',str(dest/'source/verify.py')],capture_output=True,text=True)
    (dest/'verification/verification-initial.json').write_text(p.stdout)
    if p.returncode:raise ValueError(p.stdout)
    for name in ['Run-A','Run-B','Run-C']:
        path=dest/name/'run_receipt.json';d=json.loads(path.read_text());d['verification_result']='PASS';path.write_text(json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n')
    p=subprocess.run([sys.executable,'-B',str(dest/'source/verify.py')],capture_output=True,text=True)
    (dest/'verification/verification-final.json').write_text(p.stdout)
    if p.returncode:raise ValueError(p.stdout)
    print('PASS: fresh experiment and independent checks complete at '+str(dest))

if __name__=='__main__':main()
