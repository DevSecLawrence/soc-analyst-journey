# Month 1 Demo Reel — SOC Analyst Journey
 
**Analyst:** Lawrence (Okoli Chiemerie Lawrence)
**Period:** Days 1–30, Month 1
**GitHub:** github.com/DevSecLawrence/soc-analyst-journey
 
---
 
> This document is a single-page showcase of the strongest work from Month 1. If you're a recruiter, hiring manager, or mentor — this is where to start.
 
---
 
## Best Analysis Work
 
### Phishing Email Investigation — BTLO (10/10)
**Day 24 | Blue Team Labs Online | Easy | 10/10 points**
 
Investigated a real phishing email forwarded to the SOC. Found a nested `.eml` attachment — a deliberate scanner evasion technique — containing a malicious Blogspot URL. Extracted all IOCs, ran reverse DNS on the sending IP, used URL2PNG to safely preview the destination without visiting it.
 
**What made it interesting:** The malicious URL wasn't in the email body. It was inside an attachment inside the email — two layers deep, specifically to bypass scanners that only inspect the top-level message.
 
→ [Full investigation notes](../day-24/day24-btlo-phishing.md)
→ [Incident report (3 formats)](../day-24/day24-incident-report.md)
 
---

