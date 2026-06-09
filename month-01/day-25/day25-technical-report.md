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
 
 ## Technical Findings
 
### Email Headers
 
| Field | Value |
|-------|-------|
| Recipient | `kinnar1975@yahoo.co.uk` |
| Subject | `Undeliverable: Website contact form submission` |
| Sending IP resolved host | `c5s2-1e-syd.hosting-services.net.au` |
| Encoding | `base64` |
 
The subject line is a social engineering lure — a fake bounce notification. The goal is to make the target believe a legitimate email they sent has failed to deliver, prompting them to open the attachment to investigate.

### Attachment Analysis
 
The attachment was a `.eml` file named `Website contact form submission.eml` — a second email embedded inside the first. This nested structure is a deliberate evasion technique. Many email scanners only inspect the top-level message and don't recursively parse attachments.
 
Inside the nested `.eml`, the following malicious URL was found:
 
```
https://35000usdperwwekpodf.blogspot.sg?p=3D9swg
```
 
 ### Destination Analysis
 
The malicious URL resolves to a Blogspot page — Google's free blogging platform. Attackers use free hosting services for three reasons:
 
1. Free and fast to set up with no identity verification
2. Google's domain reputation bypasses many URL filtering tools
3. Easy to take down and rebuild on a new subdomain
URL2PNG confirmed the page existed but has since been removed. Heading at time of capture: `Blog has been removed`.
 
---
 
 