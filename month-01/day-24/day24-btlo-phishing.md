# Day 24 — Blue Team Labs Online: Phishing Email Investigation
 
**Date:** 2026-06-08
**Platform:** Blue Team Labs Online (free tier)
**Challenge:** Phishing Analysis
**Difficulty:** Easy
**Points:** 10/10
**Completed:** ✅

---

## Scenario
 
A user received a phishing email and forwarded it to the SOC. Investigate the email and attachment to collect useful artifacts.
 
---
 
## Initial Hypothesis
 
Before opening the file — the scenario says "phishing email forwarded to SOC." My assumption was this would be a credential harvesting attempt, probably impersonating a well known brand, with a link to a fake login page. Classic phishing playbook.
 
That turned out to be partially right but with a twist — it wasn't a direct link to a fake login. It had a nested attachment with the malicious URL buried inside it.
 
---

