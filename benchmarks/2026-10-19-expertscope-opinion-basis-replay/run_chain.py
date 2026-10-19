#!/usr/bin/env python3
import json,platform,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def main():
 inp=Path(sys.argv[1]).resolve(); out=Path(sys.argv[2]).resolve(); out.mkdir(parents=True,exist_ok=True); stages=[("sourcebinder.py",[inp,out/"sourcebinder.json"]),("opinionmapper.py",[inp,out/"sourcebinder.json",out/"opinionmapper.json"]),("causationboundary.py",[inp,out/"opinionmapper.json",out/"causationboundary.json"]),("verdictbridge.py",[inp,out/"sourcebinder.json",out/"opinionmapper.json",out/"causationboundary.json",out/"final_chain.json"])]; records=[]
 for script,args in stages:
  start=datetime.now(timezone.utc).isoformat(); p=subprocess.run([sys.executable,"-B",str(ROOT/script),*map(str,args)],capture_output=True,text=True); (out/(script.replace(".py",".stdout.txt"))).write_text(p.stdout); (out/(script.replace(".py",".stderr.txt"))).write_text(p.stderr); records.append({"script":script,"command":[sys.executable,"-B",script,*map(str,args)],"started_utc":start,"finished_utc":datetime.now(timezone.utc).isoformat(),"exit_code":p.returncode});
  if p.returncode: break
 exec_rec={"schema":"expertscope-execution-v1","started_utc":records[0]["started_utc"],"finished_utc":datetime.now(timezone.utc).isoformat(),"python":sys.version.split()[0],"platform":platform.platform(),"stage_runs":records}; (out/"execution.json").write_text(json.dumps(exec_rec,sort_keys=True,indent=2)+"\n"); raise SystemExit(0 if len(records)==4 and all(x["exit_code"]==0 for x in records) else 1)
if __name__=="__main__": main()
