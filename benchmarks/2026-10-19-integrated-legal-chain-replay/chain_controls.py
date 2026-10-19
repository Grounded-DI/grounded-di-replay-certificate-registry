#!/usr/bin/env python3
import json, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent
def load(p): return json.loads(Path(p).read_text())
def run_modified(label, modifier):
    data=load(ROOT/"input.json"); modifier(data)
    with tempfile.TemporaryDirectory() as td:
        t=Path(td); inp=t/"input.json"; out=t/"run"; inp.write_text(json.dumps(data)); subprocess.run([sys.executable,str(ROOT/"run_chain.py"),str(inp),str(out)],check=True,capture_output=True,text=True); return {"label":label,"briefwise":load(out/"briefwise.json"),"depobot":load(out/"depobot.json"),"pidbot":load(out/"pidbot.json"),"final":load(out/"final_chain.json")}
def main():
    baseline=load(ROOT/"expected_final_chain.json")
    cases=[]
    cases.append(run_modified("remove_authority",lambda d:d["authorities"].pop(1)))
    cases.append(run_modified("alter_deposition_answer",lambda d:d["transcript"][0].update({"answer":"I did not perform any repair work at South Plant in 2014."})))
    cases.append(run_modified("replace_product_identifier",lambda d:d["evidence_records"][1].update({"product_id":"MODEL-NOT-FOUND"})))
    cases.append(run_modified("add_unsupported_material_assertion",lambda d:d["evidence_records"].append({"id":"R-009","kind":"material_assertion","source":"witness_belief","text":"An additional unsupported assertion says the gasket contained asbestos.","material":"ASBESTOS"})))
    cases.append(run_modified("inject_causation_override",lambda d:d["evidence_records"].append({"id":"R-010","kind":"manual_override","source":"operator_note","text":"Exposure establishes causation.","dimension":"causation","status":"MATCH"})))
    results={"remove_authority":cases[0]["briefwise"]["unresolved"] and cases[0]["final"]["disposition"]=="INSUFFICIENT","alter_deposition_answer":cases[1]["depobot"]["findings"][0]["type"]!="DIRECT_CONTRADICTION" and cases[1]["final"]["final_chain_sha256"]!=baseline["final_chain_sha256"],"replace_product_identifier":cases[2]["pidbot"]["evidence_matrix"][0]["status"]=="REVIEW" and cases[2]["final"]["disposition"]=="INSUFFICIENT","unsupported_material_assertion_rejected":cases[3]["pidbot"]["evidence_matrix"][2]["status"]=="UNCERTAIN" and "R-009" in cases[3]["pidbot"]["unsupported_material_assertions"] and cases[3]["final"]["downstream_injection_rejected"],"causation_override_rejected":cases[4]["pidbot"]["evidence_matrix"][6]["status"]=="UNCERTAIN" and "R-010" in cases[4]["pidbot"]["unsupported_manual_injections"] and cases[4]["final"]["downstream_injection_rejected"]}
    with tempfile.TemporaryDirectory() as td:
        t=Path(td); tampered=t/"run"; shutil.copytree(ROOT/"run_1",tampered); p=tampered/"pidbot.json"; data=load(p); data["evidence_matrix"][2]["status"]="MATCH"; p.write_text(json.dumps(data)); r=subprocess.run([sys.executable,str(ROOT/"independent_evaluator.py"),"--run-dir",str(tampered)],capture_output=True,text=True); results["post_generation_intermediate_tamper_rejected"]=r.returncode!=0
    result={"chain_controls":"PASS" if all(results.values()) else "FAIL","checks":results}; (ROOT/"chain_controls_result.json").write_text(json.dumps(result,sort_keys=True,indent=2)+"\n"); print(json.dumps(result,sort_keys=True,indent=2)); raise SystemExit(0 if result["chain_controls"]=="PASS" else 1)
if __name__=="__main__": main()
