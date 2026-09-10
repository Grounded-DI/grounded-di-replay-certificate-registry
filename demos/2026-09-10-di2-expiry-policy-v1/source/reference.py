"""Separately written evaluator: imports no kernel or kernel schema helpers.
Shared with kernel: codec.py byte serialization/hash primitives only.
Authored in the same Codex task; not an external independent audit.
"""
import re
from codec import canonical,sha

def evaluate(report,p,a,q,t):
    fixed={'action':'export_report','destination':'approved/report.txt','scope':'demo_directory','state':{'classification':'synthetic','revision':1}}
    keys={'action','destination','scope','state'}
    def number(v):return type(v)==int and v in range(0,9007199254740992)
    def shape(v):
        if not isinstance(v,dict) or set(v)!=keys:return False
        if not all(type(v[n])==str and len(v[n])>0 for n in ('action','destination','scope')):return False
        s=v['state']
        return type(s)==dict and set(s)=={'classification','revision'} and type(s['classification'])==str and number(s['revision'])
    def projection(v):return {n:v[n] for n in keys}
    reason=None
    if type(p)!=dict or set(p)!=keys|{'version','export_enabled','max_bytes'}:
        reason='POLICY_INVALID'
    elif not shape(projection(p)) or type(p['version'])!=str or not p['version'] or type(p['export_enabled'])!=bool or not number(p['max_bytes']) or p['max_bytes']==0:
        reason='POLICY_INVALID'
    elif type(a)!=dict or set(a)!=keys|{'issued_at','expires_at','report_sha256','policy_sha256'}:
        reason='AUTHORIZATION_INVALID'
    elif not shape(projection(a)) or not all(type(a[n])==str and re.fullmatch(r'[a-f0-9]{64}',a[n]) for n in ('policy_sha256','report_sha256')) or not all(number(a[n]) for n in ('issued_at','expires_at')) or a['expires_at']<=a['issued_at']:
        reason='AUTHORIZATION_INVALID'
    elif not number(t):reason='TIME_INVALID'
    elif not shape(q):reason='ACTION_INVALID'
    elif a['policy_sha256']!=sha(canonical(p)):reason='POLICY_HASH_MISMATCH'
    elif a['report_sha256']!=sha(report):reason='REPORT_HASH_MISMATCH'
    elif t<a['issued_at']:reason='NOT_YET_VALID'
    elif not t<a['expires_at']:reason='EXPIRED'
    elif q!=projection(a):reason='ACTION_BINDING_MISMATCH'
    elif q!=projection(p):reason='POLICY_SCOPE_MISMATCH'
    elif canonical(q)!=canonical(fixed):reason='UNSUPPORTED_ACTION'
    elif p['export_enabled']==False:reason='EXPORT_DISABLED'
    elif p['max_bytes']<len(report):reason='REPORT_TOO_LARGE'
    return {'decision':'DENY' if reason else 'ALLOW','reason':reason or 'AUTHORIZED'}
