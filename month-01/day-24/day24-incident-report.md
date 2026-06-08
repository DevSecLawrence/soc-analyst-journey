# Incident Report — Phishing Email Investigation
 
**Date:** 2026-06-08
**Analyst:** Lawrence
**Platform:** Blue Team Labs Online
**Challenge:** Phishing Analysis
**Classification:** Phishing / Social Engineering
 
---
 
## Executive Summary
 
A user received a phishing email disguised as a delivery failure notification. The email contained a nested `.eml` attachment with a malicious Blogspot URL inside it. The attack used a double-layer approach to evade automated email scanning. The malicious page has since been taken down but the infrastructure and IOCs have been documented.
 
---

## Timeline of Events
 
| Time | Event |
|------|-------|
| Unknown | Attacker sets up malicious Blogspot page at `35000usdperwwekpodf.blogspot.sg` |
| Unknown | Attacker crafts phishing email disguised as delivery failure notice |
| Received | Email sent to `kinnar1975@yahoo.co.uk` from Australian hosting infrastructure |
| Post-receipt | User forwards email to SOC for investigation |
| Investigation | SOC analyst opens `.eml` in VS Code, extracts headers and attachment |
| Investigation | Nested `.eml` attachment opened — malicious URL identified |
| Investigation | URL2PNG used to safely preview the Blogspot page |
| Confirmed | Blogspot page already taken down — heading: "Blog has been removed" |
 
---
 
 ## Root Cause Analysis
 
The attack relied on two social engineering techniques:
 
**1. Delivery failure lure** — The subject line `Undeliverable: Website contact form submission` tricks the target into thinking a legitimate email they sent has bounced. This creates urgency and a legitimate reason to open the attachment.
 
**2. Nested attachment evasion** — The malicious URL was not in the main email body but inside a `.eml` file attached to the email. This adds a layer that some automated email scanners miss if they only inspect the top-level message.
 
**3. Trusted infrastructure abuse** — The malicious page was hosted on Blogspot (Google). Many email security tools whitelist Google domains. Hosting malicious content on Blogspot means the domain itself won't trigger a URL block.
 
---
 
 ## IOCs
 
| Type | Value |
|------|-------|
| Sender email | Unknown (sending via hosting provider) |
| Sending infrastructure | `c5s2-1e-syd.hosting-services.net.au` |
| Recipient | `kinnar1975@yahoo.co.uk` |
| Subject | `Undeliverable: Website contact form submission` |
| Attachment name | `Website contact form submission.eml` |
| Malicious URL | `https://35000usdperwwekpodf.blogspot.sg?p=3D9swg` |
| Malicious domain | `35000usdperwwekpodf.blogspot.sg` |
| Hosting platform | Blogspot (Google) |
 
---
 