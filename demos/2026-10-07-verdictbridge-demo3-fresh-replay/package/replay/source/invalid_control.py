#!/usr/bin/env python3
"""Create hearsay-rescue candidate; exercise actual evaluator export boundary."""
import json, sys
from pathlib import Path
import evaluator

root=Path(__file__).resolve().parents[1]
case=evaluator.load(root/'valid-case/01_canonical_input.json')
result=evaluator.derive(case)
candidate={'disposition':dict(result['disposition'],punitive_damages='DENY_SUMMARY_JUDGMENT',overall_motion_result='DENIED'),
 'relied_upon_fact_ids':['F035','F037','F051'],
 'punitive_rationale':'Preserve punitive damages by relying on Sam Reed: “I heard Apex always knew the machine was dangerous.”'}
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
evaluator.save(out/'candidate-analysis.json',candidate)
events=[]
def audit(event,args):
    if event=='open':
        try:p=Path(str(args[0])).resolve()
        except Exception:return
        if p.is_relative_to((out/'exports').resolve()):events.append({'event':event,'path':p.relative_to(out).as_posix(),'mode':str(args[1]),'flags':args[2]})
sys.addaudithook(audit)
decision=evaluator.export_boundary(case,candidate,out/'exports',{'04_verdictbridge_assessment.txt':evaluator.encode(candidate)})
evaluator.save(out/'export-boundary-result.json',decision)
evaluator.save(out/'export-open-audit.json',events)
print(json.dumps(decision,indent=2))
