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
 