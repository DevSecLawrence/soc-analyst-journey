# Day 45 — Halfway Checkpoint: Honest Skill Assessment
 
**Date:** 2026-07-15
**Days completed:** 44 of 180
**Note:** Took a month break for university exams (June → July 2026). Returning to the roadmap today.
 
---
 
## Coming Back After a Month
 
I didn't plan for a month gap. Exams hit harder than I expected and the roadmap had to pause. The honest thing to document is what that break revealed — what stuck and what faded.
 
The concepts that stuck without any review: phishing investigation methodology, the MITRE ATT&CK framework, the difference between EDR and SIEM, and the shared responsibility model for cloud. Those are in my head permanently now.
 
What faded: specific Splunk SPL syntax, the exact YARA rule syntax, specific Event IDs for lateral movement detection. Those need to be re-touched before I'd be comfortable discussing them in an interview.
 
That's actually useful information, coz It tells me what genuinely stayed with me versus what I memorised temporarily. Month 2 going forward needs to focus on the things that faded — not re-learning them from scratch, but reinforcing them through more hands-on work so they stick properly in my head.
 
---

## Skills Matrix — Day 28 vs Day 45
 
| Skill | Day 28 Rating | Day 45 Rating | Change | Notes |
|-------|--------------|--------------|--------|-------|
| Log analysis | 4 | 4 | → | Solid — this stuck well |
| Splunk SPL | 3 | 2 | ↓ | Syntax faded after the break — needs reinforcement |
| MITRE ATT&CK | 4 | 4 | → | Framework understanding is permanent |
| Phishing analysis | 4 | 4 | → | Did it hands-on enough that it stuck |
| YARA rules | 3 | 2 | ↓ | Syntax faded — concepts solid |
| Sigma rules | 4 | 3 | ↓ | Concepts there, specific syntax needs review |
| EDR concepts | 1 | 2 | ↑ | Day 32 research moved the needle |
| Cloud security (AWS) | 1 | 2 | ↑ | Day 43 — foundational understanding now |
| Cloud security (Azure) | 1 | 2 | ↑ | Day 44 — know the services and model |
| Lateral movement detection | 1 | 2 | ↑ | Day 40 — concepts and detection logic |
| Persistence mechanisms | 1 | 2 | ↑ | Day 38 — know the 5 mechanisms |
| Threat hunting | 1 | 2 | ↑ | Day 42 — methodology understood |
| Exfiltration detection | 1 | 2 | ↑ | Day 41 — concepts and Sigma rules |
| Incident report writing | 3 | 4 | ↑ | Day 25 — genuinely strong now |
| Python for security | 1 | 1 | → | Haven't touched this yet |
| Active Directory | 1 | 1 | → | Haven't touched this yet |
| EDR hands-on | 0 | 0 | → | Still zero — no access to platforms |
| Security+ | 0 | 0 | → | Not started |
| Network traffic analysis | 3 | 3 | → | Wireshark work is solid |
| Detection engineering | 3 | 4 | ↑ | Month 2 research deepened this |
 
---
 
## What I Concluded
 
45 days in — including a month break — and I have more genuine knowledge than I expected. The things that stuck are the things I did hands-on: phishing investigation, MITRE mapping, Wireshark analysis, writing detection rules. The things that faded are the things I learned once and moved on from: specific syntax for Splunk, YARA, Sigma.
 
The lesson from the break: one lab is not enough to make something permanent. The concepts from Month 2's research days (EDR, persistence, lateral movement, cloud) are in my head at the concept level but I haven't touched them hands-on enough for the details to stick. Month 3 onwards needs more repetition, not more new topics.
 
The uncomfortable truth: I'm 45 days in but probably 35 days worth of genuinely retained knowledge. The break cost me something. Not everything, but something. That's honest.
 
---
 ## Assumption I Made
 
I assumed that reading and writing about techniques was enough to retain them. It's not — at least not for me. The techniques I did hands-on (phishing analysis, Wireshark, YARA rules in Kali) are solid. The ones I only read and wrote about (Splunk SPL, lateral movement Event IDs) faded during the break. Doing is the only thing that makes knowledge permanent. Month 3 needs more doing and less reading.
 
---
 
## Uncertainty I Have
 
I genuinely don't know if my self-ratings are accurate relative to what a real SOC environment would expect. I could rate myself a 3 on log analysis and still fail a technical interview because the interviewer's definition of "competent log analysis" is doing it under time pressure in a live environment, not in a controlled lab. The gap between lab skill and production skill is real and I can't measure it from where I am. That uncertainty only resolves when I'm in a real environment.
 
---
 
## Biggest Growth Areas (Days 30–45)
 
**Cloud security understanding** — went from zero to genuine conceptual understanding of AWS and Azure security models, shared responsibility, IAM/Entra ID, CloudTrail/Activity Log, and detection in cloud environments.
 
**Attack lifecycle comprehension** — understanding persistence, lateral movement, credential access, and exfiltration as a connected chain rather than isolated techniques. Days 38–41 gave me the full picture.
 
**Detection engineering depth** — writing Sigma rules for 5 persistence mechanisms, 5 lateral movement techniques, and 5 exfiltration patterns moved my detection thinking from "match known signatures" to "model attacker behaviour."
 
---
 
## Biggest Remaining Gaps
 
**Hands-on with real tools** — EDR platforms (CrowdStrike, MDE), Active Directory in a real environment, Splunk in a production-like setup. Reading about tools is not the same as using them under pressure.
 
**Python for security** — still hasn't happened. This keeps appearing in job descriptions and I keep deprioritising it. Month 3 has to include at least one working Python script for security automation.
 
**Certifications** — Security+ is still planned and still hasn't started. This needs to change in Month 3.
 
**Real incident experience** — every investigation I've done has been a challenge with a known answer. Real incidents don't have answers at the bottom. The step from "challenge solver" to "actual analyst" requires experience I can only get in a real environment or through more complex, open-ended labs.
