#!/usr/bin/env python3
"""Replay a fixed observed history; do not regenerate a scheduler order."""
import json,sys
from pathlib import Path
from codec import canonical,sha,load
from reference_check import check,files
SOURCES=['codec.py','gate.py','worker.py','run_suite.py','reference_check.py','verify.py','acceptance.py','STATE_MACHINE.md']
def identity(b):
    b=Path(b)
    derived=check(b/'evidence')
    return {'schema':'DI2-SINGLE-USE-REPLAY-1','canonicalization':'DI2-ASCII-JSON-LF-1','source_hashes':{n:sha((b/n).read_bytes()) for n in SOURCES},'report_sha256':sha((b/'report.txt').read_bytes()),'evidence_hashes':files(b/'evidence'),'derived_history_checks':derived}
def verify(b):
    b=Path(b);fresh=canonical(identity(b));expected=(b/'replay-identity.json').read_bytes()
    if fresh!=expected:raise ValueError('REPLAY_IDENTITY_MISMATCH')
    h=sha(fresh)
    if (b/'replay-identity.sha256').read_text()!=h+'\n':raise ValueError('REPLAY_SHA256_MISMATCH')
    return {'status':'PASS','replay_sha256':h,'canonical_bytes_identical':True,'scenario_count':14,'method':'Separate reference transition checker; no gate or worker imports. Shared codec primitives. Recorded order replay, not scheduler regeneration.'}
if __name__=='__main__':
    try:print(json.dumps(verify(sys.argv[1] if len(sys.argv)>1 else Path(__file__).parent),indent=2))
    except Exception as e:print(json.dumps({'status':'FAIL','reason':str(e)}));sys.exit(1)
