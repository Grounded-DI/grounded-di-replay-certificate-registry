import argparse, decimal, hashlib, json, pathlib, re, sys

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",default="fixture.json")
    p.add_argument("--source",default="source_excerpt.txt")
    p.add_argument("--config",default="config.json")
    p.add_argument("--out",required=True)
    a=p.parse_args()
    try:
        config=json.loads(pathlib.Path(a.config).read_text())
        source_hash=hashlib.sha256(pathlib.Path(a.source).read_bytes()).hexdigest()
        if source_hash!=config["source_sha256"]:
            print("SOURCE_MISMATCH",file=sys.stderr); return 2
        if config["threshold_mg_per_l_as_n"]!="10":
            print("INVALID_CONFIG",file=sys.stderr); return 2
        input_bytes=pathlib.Path(a.input).read_bytes()
        input_hash=hashlib.sha256(input_bytes).hexdigest()
        data=json.loads(input_bytes)
        samples=data["samples"]
        if not isinstance(samples,list): raise ValueError("samples must be list")
        seen=set(); results=[]
        for sample in samples:
            ident=sample["id"]
            if not isinstance(ident,str) or not ident or ident in seen: raise ValueError("invalid id")
            seen.add(ident)
            if sample.get("unit")!="mg/L as N":
                status,reason="HOLD","UNSUPPORTED_OR_MISSING_UNIT"
            elif not isinstance(sample.get("value"),str) or not re.fullmatch(r"[0-9]+(?:\.[0-9]+)?",sample["value"]):
                status,reason="HOLD","INVALID_OR_MISSING_VALUE"
            elif decimal.Decimal(sample["value"])>decimal.Decimal("10"):
                status,reason="REVIEW_ABOVE","VALUE_ABOVE_THRESHOLD"
            else:
                status,reason="AT_OR_BELOW","VALUE_AT_OR_BELOW_THRESHOLD"
            results.append({"id":ident,"status":status,"reason":reason})
        out={"input_sha256":input_hash,"source_sha256":source_hash,"results":results}
        path=pathlib.Path(a.out); path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(out,sort_keys=True,separators=(",",":"))+"\n")
        print("OK"); return 0
    except (OSError,ValueError,KeyError,TypeError,decimal.InvalidOperation) as e:
        print("INPUT_ERROR: "+str(e),file=sys.stderr); return 2

if __name__=="__main__": sys.exit(main())
