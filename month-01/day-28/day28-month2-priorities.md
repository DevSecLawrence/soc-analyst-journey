# Day 28 — Month 2 Priorities
 
**Date:** 2026-06-10
**Based on:** Skills matrix gap analysis from Day 28
 
---
 
## What Month 2 Needs to Fix
 
Month 1 gave me the foundation. I can read logs, write detection rules, investigate phishing emails, and document findings professionally. That's real. But the skills matrix showed me exactly where the gaps are — and some of them are critical for the remote roles I'm targeting.
 
Month 2 is not about learning new things for the sake of it. It's about closing the gaps that actually matter for getting hired.
 
---
 
## Priority 1 — EDR Platforms (Critical)
 
**Gap:** Zero hands-on experience with CrowdStrike, Carbon Black, or SentinelOne. Came up in 7/10 job descriptions.
 
**Why it exists:** EDR platforms require enterprise licenses or specific lab environments. They're not easy to access for free as a student.
 
**Plan:**
- LetsDefend has EDR-related challenges — work through them
- CrowdStrike has a free trial for their Falcon platform — explore it
- Focus on understanding EDR concepts (process injection detection, behavioural analysis, alert triage) even if hands-on access is limited
- Document everything I learn about EDR workflows even if it's conceptual
**Critical or nice-to-have:** Critical. This is the biggest gap between where I am and where I need to be.
 
---

## Priority 2 — Active Directory (Critical)
 
**Gap:** Know what it is, never administered or attacked/defended it. Came up in 4/10 job descriptions but is fundamental to enterprise environments.
 
**Plan:**
- TryHackMe has free Active Directory rooms — work through them
- Set up a basic AD lab in VirtualBox once the local lab is rebuilt (Domain Controller + Windows 10 client)
- Learn common AD attack techniques — Pass the Hash, Kerberoasting, DCSync — from a defender's perspective
- Map findings to MITRE ATT&CK
**Critical or nice-to-have:** Critical for enterprise SOC roles. Slightly less critical for cloud-first companies.
 
---
 
## Priority 3 — Python for Security (High Priority)
 
**Gap:** Know Python basics from uni, never applied it to security. Came up in 5/10 job descriptions.
 
**Why it exists:** University Python is academic. Security Python is practical. I never bridged the gap.
 
**Plan:**
- Write small scripts that automate things I'm already doing manually — IOC extraction from emails, log parsing, hash lookups via VirusTotal API
- Start simple: a script that reads a .eml file and extracts all URLs and IPs automatically
- Document each script in GitHub with what it does and why I wrote it
**Critical or nice-to-have:** High priority. Automation is increasingly expected even at Tier 1.
 
---
 
## Priority 4 — Cloud Security Fundamentals (Medium Priority)
 
**Gap:** No AWS or Azure experience. Came up in 6/10 job descriptions.
 
**Plan:**
- AWS has a free tier — spin up a basic environment and explore CloudTrail logs (AWS's equivalent of Windows Event Logs)
- Microsoft Azure has free credits for students — explore Azure Sentinel (now Microsoft Sentinel), which is a cloud SIEM
- Focus on log sources and detection in cloud environments, not infrastructure management
**Critical or nice-to-have:** Medium. More critical for cloud-first companies, less so for traditional enterprise SOC roles. Still worth understanding the basics.
 
---

## Priority 5 — Security+ (High Priority)
 
**Gap:** No certification. Came up in 5/10 job descriptions and directly affects salary bands.
 
**Plan:**
- Target sitting the exam at the end of Month 4 or start of Month 5
- Use Professor Messer's free Security+ course on YouTube alongside the roadmap
- Don't let exam prep replace hands-on work — do both in parallel
- Budget for the exam voucher now so it's not a surprise
**Critical or nice-to-have:** High priority. Not urgent for Month 2 but needs to be in progress.
 
---
 
## Month 2 Focus Summary
 
| Priority | Topic | Urgency |
|----------|-------|---------|
| 1 | EDR platforms | Critical |
| 2 | Active Directory | Critical |
| 3 | Python for security | High |
| 4 | Cloud security basics | Medium |
| 5 | Security+ prep | High |
 
---
 
## What I'm NOT Adding to Month 2
 
Malware analysis, firewall configuration, IDS/IPS — these came up in job descriptions but they're not as common in remote junior SOC roles as the 5 priorities above. I'll get to them but they're not Month 2 material.
 
Month 2 is about closing the gaps that are blocking me from applying with confidence. Everything else comes after.