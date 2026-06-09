# Technical Incident Report — Phishing Email Investigation
 
**Date:** 2026-06-08
**Analyst:** Lawrence
**Severity:** Medium
**Status:** Closed — malicious infrastructure taken down
**Reference:** BTLO Phishing Analysis Challenge
 
---
 
## Incident Overview
 
A user (`kinnar1975@yahoo.co.uk`) received a phishing email disguised as a delivery failure notification. The email contained a nested `.eml` attachment. The malicious URL was inside that nested attachment, not in the main email body. The destination page was hosted on Blogspot and has since been taken down. No confirmed credential compromise — investigation was conducted on the forwarded email artifact only.
 
---

## Timeline
 
| Timestamp | Event |
|-----------|-------|
| Unknown | Attacker registers Blogspot page at `35000usdperwwekpodf.blogspot.sg` |
| Unknown | Phishing email crafted and sent to target |
| Received | Email received by `kinnar1975@yahoo.co.uk` |
| Post-receipt | User forwards email to SOC for triage |
| Investigation | `.eml` file opened in VS Code — headers extracted |
| Investigation | Sending IP identified — reverse DNS run via whois.domaintools.com |
| Investigation | Nested `.eml` attachment opened — malicious URL extracted |
| Investigation | URL2PNG used to safely preview destination page |
| Confirmed | Destination page already taken down — "Blog has been removed" |
 
---
 