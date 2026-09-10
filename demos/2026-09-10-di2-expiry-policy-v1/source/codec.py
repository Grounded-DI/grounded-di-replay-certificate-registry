"""DI2-ASCII-JSON-LF-1; byte utilities only, no decision logic."""
import hashlib,json
from pathlib import Path

def canonical(value):
    def check(x):
        if x is None or type(x) is bool:return
        if type(x) is int and abs(x)<=9007199254740991:return
        if type(x) is str and all(32<=ord(c)<=126 or c=='\n' for c in x):return
        if type(x) is list:
            for item in x:check(item)
            return
        if type(x) is dict:
            for k,v in x.items():
                if type(k) is not str:raise ValueError('NON_STRING_KEY')
                check(k);check(v)
            return
        raise ValueError('UNSUPPORTED_CANONICAL_VALUE')
    check(value)
    return (json.dumps(value,sort_keys=True,ensure_ascii=True,separators=(',',':'),allow_nan=False)+'\n').encode('ascii')
def sha(data):return hashlib.sha256(data).hexdigest()
def load(path):
    def unique(pairs):
        out={}
        for k,v in pairs:
            if k in out:raise ValueError('DUPLICATE_JSON_KEY')
            out[k]=v
        return out
    return json.loads(Path(path).read_text(encoding='utf-8'),object_pairs_hook=unique,parse_constant=lambda x:(_ for _ in ()).throw(ValueError('NONFINITE_JSON')))
def save(path,value):Path(path).write_bytes(canonical(value))
