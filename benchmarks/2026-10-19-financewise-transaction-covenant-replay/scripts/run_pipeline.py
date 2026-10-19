import argparse
import json
import subprocess
import sys
from pathlib import Path

def main():
    p = argparse.ArgumentParser()
    p.add_argument("input")
    p.add_argument("output_dir")
    a = p.parse_args()
    root = Path(__file__).resolve().parent
    out = Path(a.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    stage = root / "finance_stage_v2.py"
    steps = [
        ("recordbinder", ["binder", a.input, out / "recordbinder.json"]),
        ("transactionresolver", ["resolver", a.input, out / "transactionresolver.json"]),
        ("accountingboundary", ["account", a.input, out / "accountingboundary.json", "--resolver", out / "transactionresolver.json"]),
        ("covenantbridge", ["covenant", a.input, out / "covenantbridge.json", "--resolver", out / "transactionresolver.json", "--accounting", out / "accountingboundary.json"]),
    ]
    for name, args in steps:
        q = subprocess.run([sys.executable, str(stage)] + [str(x) for x in args], cwd=root, text=True, capture_output=True, check=False)
        (out / f"{name}.stdout.txt").write_text(q.stdout, encoding="utf-8")
        (out / f"{name}.stderr.txt").write_text(q.stderr, encoding="utf-8")
        if q.returncode:
            raise SystemExit(q.returncode)
    resolver = json.loads((out / "transactionresolver.json").read_text())
    account = json.loads((out / "accountingboundary.json").read_text())
    covenant = json.loads((out / "covenantbridge.json").read_text())
    final = {
        "schema": "financewise-final-chain-v2",
        "stage_files": ["recordbinder.json", "transactionresolver.json", "accountingboundary.json", "covenantbridge.json"],
        "measured_cash": account["measured_cash"],
        "measured_current_liabilities": account["measured_current_liabilities"],
        "measured_ratio": covenant["ratio"],
        "arithmetic_result": covenant["arithmetic_result"],
        "unresolved_items": covenant["unresolved_items"],
        "disposition": covenant["disposition"],
        "stage_statuses": {
            "RecordBinder": json.loads((out / "recordbinder.json").read_text())["status"],
            "TransactionResolver": resolver["status"],
            "AccountingBoundary": account["status"],
            "CovenantBridge": covenant["disposition"],
        },
        "derived_from": "input records and specification; no injected disposition accepted",
    }
    (out / "final_chain.json").write_text(json.dumps(final, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(final, sort_keys=True))

if __name__ == "__main__":
    main()
