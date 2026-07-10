# Day 41 — Exfiltration Techniques Reference
 
**Date:** 2026-06-22
 
---
 
## Quick Reference Table

I built this table from ATT&CK technique pages first, then mapped each one to detection signals I can actually monitor.

![MITRE ATT&CK T1048 page used while building the exfiltration quick reference mapping](./screenshots/Screenshot%202026-07-10%20204715.png)
 
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

I ranked DNS tunneling first after checking ATT&CK plus Unit 42's practical abuse examples.

![Unit 42 DNS tunneling research used to validate why DNS tunneling has a strong anomaly signal](./screenshots/Screenshot%202026-07-10%20204901.png)
 
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
## The Baseline Problem
 
Every exfiltration detection rule I've written has a version of the same problem — it needs a threshold, and the threshold depends on knowing what normal looks like.
 
| Detection | Threshold needed | Baseline challenge |
|-----------|-----------------|-------------------|
| Large outbound upload | X MB per hour | Varies by role — a video editor vs an accountant have very different normal volumes |
| DNS query frequency | N queries per minute to same domain | Varies by software — some apps are legitimately chatty with DNS |
| Cloud upload volume | Y MB per day | Varies by whether the user actively uses cloud storage for work |
| Email attachment size | Z MB per recipient | Varies by department — some teams send large files regularly |
 
Without per-user and per-machine baselines, any fixed threshold will either miss attacks or flood analysts with false positives.
 
---
## What Legitimate Traffic Looks Like vs Exfiltration
 
| Behaviour | Legitimate | Exfiltration |
|-----------|-----------|-------------|
| Cloud upload | Regular, consistent destination, during work hours, from cloud-enabled machine | Sudden large upload, new destination, off hours, from machine with no prior cloud activity |
| DNS queries | Short subdomains, consistent patterns, match known applications | Long random subdomains, high entropy, high volume to single domain |
| Email attachments | Known recipients, consistent size range, business content types | External recipients never contacted before, unusual file types, off-hours |
| ICMP traffic | Small, infrequent pings | Large payloads, sustained over time, consistent intervals |