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
