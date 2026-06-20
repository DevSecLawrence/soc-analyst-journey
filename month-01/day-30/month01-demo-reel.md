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

### Sysmon Attack Chain Investigation — LetsDefend
**Day 23 | LetsDefend | 757 Sysmon events**
 
Investigated a compromised Windows endpoint. Traced the full attack chain through Sysmon event logs — identified initial access via IDM.exe spawning shells, UAC bypass via fodhelper.exe (auto-elevation without prompting), and persistence via registry run keys.
 
**Key findings:**
 
| Finding | Detail | MITRE |
|---------|--------|-------|
| Initial access | IDM.exe spawning cmd.exe | T1566 |
| UAC bypass | fodhelper.exe | T1548.002 |
| Persistence | HKCU\...\CurrentVersion\Run | T1547.001 |
 
→ [Full investigation notes](../day-23/day23-sysmon-analysis.md)
 
---
 
### Network Analysis — Web Shell — BTLO
**Day 29 | Blue Team Labs Online | Wireshark PCAP**
 
Traced a full web application attack chain from a single PCAP file — port scan, directory brute force, PHP web shell upload, command execution, and reverse shell establishment. Attack chain visible end to end in Wireshark with the right filters.
 
→ [Full investigation notes](../day-29/day29-btlo-webshell.md)
 
---
 
## Detection Rules
 
### YARA Rules Collection
**Day 22 | Kali Linux | YARA 4.5.5**
 
3 original rules written from scratch and tested against real files:
- `suspicious_strings.yar` — detects cmd.exe/powershell.exe references
- `high_entropy.yar` — flags files above 7.0 entropy (possible packing/encryption)
- `unusual_pe_sections.yar` — detects UPX-packed binaries by section name
→ [yara-rules-collection repo](https://github.com/DevSecLawrence/yara-rules-collection)
→ [Day 22 write-up](../day-22/day22-yara-rules.md)
 
---

### Sigma Rules Collection
**Days 20–21 | Converted to Splunk SPL and Elastic KQL**
 
Detection rules covering:
- PowerShell abuse (T1059.001) — encoded commands, download cradles
- System recon (T1033) — whoami execution post-compromise
- Persistence (T1136.001) — new local admin account creation
→ [sigma-rules-collection repo](https://github.com/DevSecLawrence/sigma-rules-collection)
 
---
 
## Professional Reports
 
### Phishing Incident — 3 Audiences, 3 Formats
**Day 25 | Based on Day 24 BTLO investigation**
 
The same phishing incident rewritten three completely different ways:
 
**Technical report (SOC manager)** — full detail, timeline, IOC table, MITRE mapping, confidence levels, recommendations
 
**Executive summary (CISO)** — one paragraph, no jargon, business risk, clear action items
 
**User email (affected user)** — three sentences, plain English, no blame, one specific question
 
This is the document I'm most proud of from Month 1. Finding the incident is half the job. The other half is explaining it clearly to the right person.
 
→ [Technical report](../day-25/day25-technical-report.md)
→ [Executive summary](../day-25/day25-executive-summary.md)
→ [User email](../day-25/day25-user-email.md)
→ [incident-reports repo](https://github.com/DevSecLawrence/incident-reports)
 
---

