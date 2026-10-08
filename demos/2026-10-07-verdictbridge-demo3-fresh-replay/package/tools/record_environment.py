#!/usr/bin/env python3
"""Future reviewer helper; records a narrow environment inventory, never secrets."""
import datetime, hashlib, json, locale, os, platform, sys
from pathlib import Path
print(json.dumps({
 "recorded_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "python_version":sys.version,"implementation":platform.python_implementation(),
 "python_binary_sha256":hashlib.sha256(Path(sys.executable).read_bytes()).hexdigest(),
 "os":platform.system(),"release":platform.release(),"machine":platform.machine(),
 "locale":locale.getlocale(),"timezone_names":__import__('time').tzname,
 "environment":{k:os.environ.get(k) for k in ('LANG','LC_ALL','TZ')},
 "dependency_note":"Core reproduction uses Python standard library; no model endpoint. Record any local changes separately."
},indent=2))
