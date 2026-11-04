import argparse, decimal, hashlib, json, pathlib, re, sys

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",default="fixture.json")
    p.add_argument("--source",default="source_excerpt.txt")
    p.add_argument("--config",default="config.json")
    p.add_argument("--out",required=True)
    a=p.parse_args()
    try:
        cfg=json.loads(pathlib.Path(a.config).read_text())
        digest=hashlib.sha256(pathlib.Path(a.source).read_bytes()).hexdigest()
        if digest!=cfg["source_sha256"] or cfg["threshold_mg_per_l_as_n"]!="10":
            print("SOURCE_OR_CONFIG_MISMATCH",file=sys.stderr); return 2
        input_bytes=pathlib.Path(a.input).read_bytes()
        input_hash=hashlib.sha256(input_bytes).hexdigest()
        data=json.loads(input_bytes)
        samples=data["samples"]
        if not isinstance(samples,list): raise ValueError("samples must be list")
        actual=json.loads(pathlib.Path(a.out).read_text())
        if actual.get("input_sha256")!=input_hash:
            print("INPUT_MISMATCH",file=sys.stderr); return 1
        expected=[]; ids=set()
        for s in samples:
            ident=s["id"]
            if not isinstance(ident,str) or not ident or ident in ids: raise ValueError("invalid id")
            ids.add(ident)
            unit=s.get("unit"); value=s.get("value")
            if unit!="mg/L as N": outcome=("HOLD","UNSUPPORTED_OR_MISSING_UNIT")
            elif not isinstance(value,str) or re.fullmatch(r"[0-9]+(?:\.[0-9]+)?",value) is None:
                outcome=("HOLD","INVALID_OR_MISSING_VALUE")
            elif decimal.Decimal(value)<=decimal.Decimal("10"):
                outcome=("AT_OR_BELOW","VALUE_AT_OR_BELOW_THRESHOLD")
            else: outcome=("REVIEW_ABOVE","VALUE_ABOVE_THRESHOLD")
            expected.append({"id":ident,"status":outcome[0],"reason":outcome[1]})
        if actual!={"input_sha256":input_hash,"source_sha256":digest,"results":expected}:
            print("RESULT_MISMATCH",file=sys.stderr); return 1
        print("CHECK_OK"); return 0
    except (OSError,ValueError,KeyError,TypeError,decimal.InvalidOperation) as e:
        print("CHECK_ERROR: "+str(e),file=sys.stderr); return 2

if __name__=="__main__": sys.exit(main())
