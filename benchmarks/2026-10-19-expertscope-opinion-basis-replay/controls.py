#!/usr/bin/env python3
import json,subprocess,sys,tempfile,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def load(p): return json.loads(Path(p).read_text())
def run_case(label,mutate):
 d=load(ROOT/"input.json"); mutate(d)
 with tempfile.TemporaryDirectory() as td:
  t=Path(td); inp=t/"input.json"; inp.write_text(json.dumps(d)); out=t/"run"; p=subprocess.run([sys.executable,"-B",str(ROOT/"run_chain.py"),str(inp),str(out)],capture_output=True,text=True); outputs={n:load(out/(n+".json")) for n in ("sourcebinder","opinionmapper","causationboundary","final_chain") if (out/(n+".json")).is_file()}; return {"label":label,"exit_code":p.returncode,"outputs":outputs}
def main():
 base=load(ROOT/"expected_outputs/final_chain.json"); checks={}; cases=[]
 cases.append(run_case("remove_source_excerpt",lambda d:d["sources"].__setitem__(0,{**d["sources"][0],"text":"altered"})))
 checks["remove_or_alter_excerpt_rejected"]=cases[-1]["exit_code"]!=0
 cases.append(run_case("alter_page_binding",lambda d:d["sources"].__setitem__(3,{**d["sources"][3],"location":"page 89, lines 3-9"})))
 checks["page_binding_change_rejected"]=cases[-1]["exit_code"]!=0
 cases.append(run_case("broaden_opinion",lambda d:d["opinions"][1].update({"exact_opinion":d["opinions"][1]["exact_opinion"]+" The product definitely caused the disease."})))
 checks["opinion_broadening_rejected"]=cases[-1]["exit_code"]!=0
 cases.append(run_case("assert_missing_assumption_supported",lambda d:d["evidence_records"].append({"id":"OPERATOR-ASSERTION","kind":"assumption_override","source_id":"HIST-1","status":"present"})))
 checks["unsupported_assumption_override_no_upgrade"]=cases[-1]["exit_code"]==0 and cases[-1]["outputs"]["opinionmapper"]["opinions"][1]["assessment"]=="QUALIFIED"
 cases.append(run_case("add_unsupported_dose_causation",lambda d:d["evidence_records"].append({"id":"ASSERT-ONLY","kind":"dose_measurement","source_id":"HIST-1","status":"conclusory_assertion","text":"Dose and causation established."})))
 checks["conclusory_dose_causation_rejected"]=cases[-1]["exit_code"]==0 and cases[-1]["outputs"]["causationboundary"]["evidence_matrix"][4]["status"]=="MISSING"
 cases.append(run_case("negative_control_injection",lambda d:d["evidence_records"].append({"id":"CONTROL-INJECT","kind":"causation_record","source_id":"CONTROL-1","status":"present"})))
 checks["negative_control_not_causation"]=cases[-1]["exit_code"]==0 and cases[-1]["outputs"]["causationboundary"]["negative_control"]["affirmative_causation_proof"] is False
 def add_genuine(d):
  d["sources"] += [
   {"id":"SUPPORT-1","type":"verified_component_record","author":"Synthetic custodian","location":"exhibit PX-4","text":"Synthetic service log identifies the removed gasket as component seal S-4 fitted to Model Q-4."},
   {"id":"SUPPORT-2","type":"synthetic_material_test","author":"Synthetic laboratory","location":"report paragraph 2","text":"Synthetic component test identifies asbestos in seal S-4; scope limited to the tested sample."},
   {"id":"SUPPORT-3","type":"synthetic_hygiene_measurement","author":"Synthetic hygienist","location":"report table 1","text":"Synthetic task measurement records 0.20 units per cubic centimeter for the specified gasket-removal task; fixture measurement only."}
  ]
  d["evidence_records"] += [
   {"id":"COMP-2","kind":"component_verified","source_id":"SUPPORT-1","status":"present_verified","product":"MODEL-Q4","component":"S-4"},
   {"id":"MAT-2","kind":"material_test","source_id":"SUPPORT-2","status":"present_verified","component":"S-4","material":"synthetic asbestos fixture"},
   {"id":"EXP-2","kind":"exposure_record","source_id":"SUPPORT-1","status":"present_verified","product":"MODEL-Q4","component":"S-4"},
   {"id":"DOSE-2","kind":"dose_measurement","source_id":"SUPPORT-3","status":"present_verified","value":"0.20 synthetic units/cm3","scope":"specified task only"}
  ]
  d["opinions"][1]["assumptions"][0]["evidence_refs"]=["MAT-2"]; d["opinions"][1]["assumptions"][1]["evidence_refs"]=["EXP-2"]; d["opinions"][1]["assumptions"][2]["evidence_refs"]=["DOSE-2","HIST-1"]
 cases.append(run_case("add_genuine_supporting_records",add_genuine))
 changed=cases[-1]["outputs"]["final_chain"]
 changed_cb=cases[-1]["outputs"]["causationboundary"]
 checks["genuine_support_changes_reasoned_result"]=cases[-1]["exit_code"]==0 and changed["disposition"]=="REVIEW_REQUIRED" and changed["disposition"]!=base["disposition"] and changed_cb["evidence_matrix"][1]["status"]=="SUPPORTED" and changed_cb["evidence_matrix"][2]["status"]=="SUPPORTED" and changed_cb["evidence_matrix"][4]["status"]=="SUPPORTED"
 with tempfile.TemporaryDirectory() as td:
  t=Path(td); shutil.copytree(ROOT/"run_1",t/"tampered"); p=t/"tampered/opinionmapper.json"; x=load(p); x["opinions"][1]["assessment"]="SUPPORTED"; p.write_text(json.dumps(x)); tampered=t/"tampered"; out=t/"rejected.json"; command=[sys.executable,"-B",str(ROOT/"verdictbridge.py"),str(ROOT/"input.json"),str(tampered/"sourcebinder.json"),str(tampered/"opinionmapper.json"),str(tampered/"causationboundary.json"),str(out)]; rejected=subprocess.run(command,capture_output=True,text=True)
  checks["post_generation_intermediate_tamper_detected"]=rejected.returncode!=0 and json.loads(out.read_text())["chain_valid"] is False
 results={"status":"PASS" if all(checks.values()) else "FAIL","checks":checks,"altered_cases":[{"label":x["label"],"exit_code":x["exit_code"]} for x in cases],"genuine_support_result":changed["disposition"]}
 (ROOT/"control_results.json").write_text(json.dumps(results,sort_keys=True,indent=2)+"\n"); print(json.dumps(results,sort_keys=True,indent=2)); raise SystemExit(0 if results["status"]=="PASS" else 1)
if __name__=="__main__": main()
