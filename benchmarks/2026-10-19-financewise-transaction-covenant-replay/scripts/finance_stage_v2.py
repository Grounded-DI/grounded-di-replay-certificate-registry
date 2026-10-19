import argparse
import hashlib
import json
from pathlib import Path
import finance_core

def write(path, value):
    Path(path).write_text(json.dumps(value, sort_keys=True, indent=2) + "\n", encoding="utf-8")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("mode", choices=["binder", "resolver", "account", "covenant"])
    p.add_argument("input")
    p.add_argument("output")
    p.add_argument("--resolver")
    p.add_argument("--accounting")
    a = p.parse_args()
    data = finance_core.load(a.input)
    input_hash = hashlib.sha256(Path(a.input).read_bytes()).hexdigest()
    if a.mode == "binder":
        bindings, errors = finance_core.source_bindings(data)
        result = {"stage": "RecordBinder", "input_sha256": input_hash, "bound_record_count": len(bindings), "rejected_record_ids": [x["record_id"] for x in errors], "bindings": bindings, "binding_errors": errors, "status": "PASS" if not errors else "REVIEW_REQUIRED"}
    elif a.mode == "resolver":
        result = finance_core.resolve(data)
        result.update({"stage": "TransactionResolver", "input_sha256": input_hash})
    elif a.mode == "account":
        resolution = json.loads(Path(a.resolver).read_text(encoding="utf-8"))
        result = finance_core.account(data, resolution)
        result.update({"stage": "AccountingBoundary", "input_sha256": input_hash})
    else:
        resolution = json.loads(Path(a.resolver).read_text(encoding="utf-8"))
        accounting = json.loads(Path(a.accounting).read_text(encoding="utf-8"))
        result = finance_core.covenant(data, resolution, accounting)
        result.update({"stage": "CovenantBridge", "input_sha256": input_hash})
    write(a.output, result)
    print(json.dumps({"stage": result["stage"], "status": result.get("status", result.get("disposition")), "ratio": result.get("ratio")}))

if __name__ == "__main__":
    main()
