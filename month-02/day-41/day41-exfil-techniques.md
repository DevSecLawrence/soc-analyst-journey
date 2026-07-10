# Day 41 — Exfiltration Techniques Reference
 
**Date:** 2026-06-22
 
---
 
## Quick Reference Table
 
| Technique | MITRE ID | Channel used | Encrypted? | Key detection signal | Common tools |
|-----------|----------|-------------|------------|---------------------|-------------|
| HTTP/HTTPS upload | T1048.003 | Web traffic | Yes (HTTPS) | Large outbound volume to unknown destination | curl, wget, PowerShell |
| DNS tunneling | T1071.004 | DNS queries | No (visible in query) | High entropy subdomains, long query strings | dnscat2, iodine |
| Cloud storage abuse | T1567.002 | HTTPS to cloud | Yes | Unusual upload pattern from unexpected machine | rclone, native clients |
| Email exfiltration | T1048 | SMTP/webmail | Sometimes | Large attachments to external addresses | Native email, SMTP scripts |
| Protocol tunneling | T1048.001 | ICMP/other | Varies | Large ICMP payloads, traffic on unusual ports | ptunnel, custom scripts |
 
---
## Detection Priority Order
 
If I had to prioritise which exfiltration technique to detect first in a real environment:
 
1. **DNS tunneling** — most detectable with entropy analysis, least legitimate use cases, clearest signal
2. **HTTP/HTTPS uploads** — volume anomalies are detectable even without content inspection
3. **Email exfiltration** — DLP at the email gateway gives content inspection capability
4. **Cloud storage abuse** — detectable via behaviour baselining, hardest to block without business impact
5. **Protocol tunneling** — niche but worth monitoring ICMP payload sizes and unusual port usage
---
 
## Network Telemetry That Matters for Exfiltration
 
The most useful data sources for exfiltration detection:
 
| Data source | What it shows |
|-------------|--------------|
| NetFlow / traffic metadata | Volume, destination, protocol, timing — without content |
| DNS logs | All queries made by every machine — essential for DNS tunneling detection |
| Proxy logs | HTTP/HTTPS destination URLs and transfer sizes |
| Email gateway logs | Attachments, recipients, volume |
| Endpoint process telemetry | Which process created the network connection — maps traffic to application |
 
---
