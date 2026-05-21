import re
import json
from datetime import datetime, timezone

# ── the log line to parse ──────────────────────────────────────
log_line = '::1 - - [20/May/2026:13:36:07 +0100] "GET / HTTP/1.1" 200 10926 "-" "curl/8.5.0"'

# ── manual regex pattern ───────────────────────────────────────
# broken down so you can read each piece:
#   (.+?)         → client IP (handles both IPv4 and IPv6)
#   \S+           → ident (ignored, always -)
#   \S+           → auth user (ignored, always -)
#   \[(.+?)\]     → timestamp in brackets
#   "(\S+)        → HTTP method
#   (\S+)         → URL
#   \S+"          → HTTP version
#   (\d{3})       → status code
#   \d+           → bytes sent (ignored for now)
#   ".*?"         → referrer (ignored)
#   "(.+?)"       → user-agent

pattern = r'(.+?) \S+ \S+ \[(.+?)\] "(\S+) (\S+) \S+" (\d{3}) \d+ ".*?" "(.+?)"'

match = re.match(pattern, log_line)

if not match:
    print("ERROR: log line did not match pattern")
    exit(1)

# ── extract fields ─────────────────────────────────────────────
client_ip   = match.group(1)
raw_ts      = match.group(2)   # 20/May/2026:13:36:07 +0100
http_method = match.group(3)
url         = match.group(4)
status_code = int(match.group(5))
user_agent  = match.group(6)

# ── convert timestamp to UTC epoch ────────────────────────────
# Apache format: 20/May/2026:13:36:07 +0100
dt = datetime.strptime(raw_ts, "%d/%b/%Y:%H:%M:%S %z")
utc_epoch = int(dt.astimezone(timezone.utc).timestamp())
utc_iso   = dt.astimezone(timezone.utc).isoformat()

# ── build output dict ──────────────────────────────────────────
parsed = {
    "client_ip":   client_ip,
    "timestamp": {
        "original":  raw_ts,
        "utc_iso":   utc_iso,
        "utc_epoch": utc_epoch
    },
    "http_method": http_method,
    "url":         url,
    "status_code": status_code,
    "user_agent":  user_agent
}

# ── print as JSON ──────────────────────────────────────────────
print(json.dumps(parsed, indent=2))
