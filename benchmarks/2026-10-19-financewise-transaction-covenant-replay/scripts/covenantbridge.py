import subprocess, sys
from pathlib import Path
if __name__ == "__main__":
    args = [sys.executable, str(Path(__file__).parent / "finance_stage_v2.py"), "covenant"] + sys.argv[1:]
    raise SystemExit(subprocess.run(args).returncode)
