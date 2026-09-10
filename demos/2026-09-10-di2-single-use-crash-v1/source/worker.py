#!/usr/bin/env python3
import json,sys,time
from pathlib import Path
from codec import load,save
from gate import handle
if __name__=='__main__':
    root,request,worker=Path(sys.argv[1]),Path(sys.argv[2]),sys.argv[3]
    barrier=None if len(sys.argv)<5 or sys.argv[4]=='-' else Path(sys.argv[4])
    crash=sys.argv[5] if len(sys.argv)>5 else None
    if barrier:
        save(barrier.parent/(worker+'.ready'),{'worker':worker})
        end=time.monotonic()+15
        while not barrier.exists():
            if time.monotonic()>end:raise RuntimeError('BARRIER_TIMEOUT')
            time.sleep(.005)
    print(json.dumps(handle(root,load(request),worker,crash)),flush=True)
