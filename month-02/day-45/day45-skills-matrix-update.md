# Day 45 — Skills Matrix Update

**Date:** 2026-07-15
**Comparison:** Day 28 matrix vs today (Day 45)
**Job descriptions reviewed:** 10 new junior SOC analyst remote postings

---

## New Job Description Analysis

Reviewed 10 fresh job postings for Junior SOC Analyst and SOC Analyst Level 1 roles targeting remote candidates. Skills that appeared most frequently:

| Skill | Frequency (10 JDs) | Day 28 Frequency | Change |
|-------|-------------------|-----------------|--------|
| Log analysis / SIEM | 10/10 | 10/10 | Same |
| Incident response | 9/10 | 8/10 | +1 |
| MITRE ATT&CK | 8/10 | 9/10 | -1 |
| EDR platforms | 8/10 | 7/10 | +1 |
| Cloud security (AWS/Azure) | 8/10 | 6/10 | +2 |
| Threat hunting | 6/10 | 3/10 | +3 |
| Python/scripting | 6/10 | 5/10 | +1 |
| Network traffic analysis | 6/10 | 8/10 | -2 |
| Active Directory | 5/10 | 4/10 | +1 |
| Security+ certification | 5/10 | 5/10 | Same |
| Detection engineering | 4/10 | 2/10 | +2 |
| Phishing analysis | 4/10 | 8/10 | -4 |

**Notable trend:** Cloud security and threat hunting appearing more frequently than they did at Day 28. The market is moving faster than the traditional on-premise SOC skill set.

---

## Full Skills Rating — Day 28 vs Day 45

| Skill | Day 28 | Day 45 | Direction |
|-------|--------|--------|-----------|
| Log analysis | 4 | 4 | → |
| Phishing analysis | 4 | 4 | → |
| Incident report writing | 3 | 4 | ↑ |
| MITRE ATT&CK | 4 | 4 | → |
| Network traffic analysis (Wireshark) | 3 | 3 | → |
| Detection engineering | 3 | 4 | ↑ |
| Sigma rules | 4 | 3 | ↓ (syntax faded) |
| YARA rules | 3 | 2 | ↓ (syntax faded) |
| Splunk SPL | 3 | 2 | ↓ (syntax faded) |
| EDR concepts | 1 | 2 | ↑ |
| Cloud security (AWS) | 1 | 2 | ↑ |
| Cloud security (Azure) | 1 | 2 | ↑ |
| Lateral movement detection | 1 | 2 | ↑ |
| Persistence mechanisms | 1 | 2 | ↑ |
| Credential access techniques | 1 | 2 | ↑ |
| Exfiltration detection | 1 | 2 | ↑ |
| Threat hunting methodology | 1 | 2 | ↑ |
| Python for security | 1 | 1 | → |
| Active Directory | 1 | 1 | → |
| EDR hands-on (CrowdStrike/MDE) | 0 | 0 | → |
| Security+ | 0 | 0 | → |

---

## What Improved vs What Faded

**Improved (new territory covered in Days 30–44):**
- Cloud security — AWS and Azure fundamentals, IAM, logging, detection concepts
- Attack lifecycle — persistence, lateral movement, credential access, exfiltration as connected chain
- Threat hunting — methodology, hypothesis-driven hunting, hunt reports

**Faded (learned once, not reinforced):**
- Splunk SPL syntax — concepts intact, specific syntax needs refreshing
- YARA rule syntax — know what rules do, specific syntax needs a lab session
- Sigma rule syntax — same as YARA

**The fading pattern is clear:** anything I only wrote about without doing repeatedly faded during the month break. Anything I did hands-on (phishing, Wireshark, YARA in Kali) stayed solid.

---

## Priority Gaps for Remaining 135 Days

| Gap | Priority | Why |
|-----|----------|-----|
| Security+ certification | Critical | Appears in 5/10 JDs, unlocks salary bands |
| EDR hands-on | Critical | 8/10 JDs — most common tool gap |
| Active Directory | High | 5/10 JDs — fundamental for enterprise SOC |
| Python for security | High | 6/10 JDs — automation increasingly expected |
| Splunk/Sigma reinforcement | High | Core skill that faded — needs repetition not re-learning |
| Real complex labs | Medium | Move from challenge-with-answers to open-ended investigation |