# Day 28 — Skills Matrix vs Job Requirements
 
**Date:** 2026-06-10
**Source:** 10 Junior SOC Analyst job descriptions from LinkedIn (remote roles)
 
---
 
## How I Rated Myself
 
- **0** — Never heard of it
- **1** — Know what it is, never used it
- **2** — Used it once or twice
- **3** — Done it in a lab setting
- **4** — Comfortable, can explain it
- **5** — Could demonstrate it in an interview right now
I tried to be honest here. It's easy to give yourself 4s and 5s when nobody's checking. But the whole point of this exercise is to know where I actually stand, not where I want to stand.
 
---
 
## Skills Matrix
 
| Skill / Tool | Times mentioned across 10 JDs | My Rating | Notes |
|---|---|---|---|
| Log analysis | 10/10 | 4 | Done this across multiple days — Windows Event Logs, Sysmon, auditd |
| SIEM (Splunk) | 9/10 | 3 | Written SPL queries, done threat hunting in lab — not production experience |
| MITRE ATT&CK | 9/10 | 4 | Used it for mapping findings on Day 15, 23 — comfortable navigating it |
| Incident response | 8/10 | 3 | Written reports, investigated real challenges — never done it in a live environment |
| Phishing analysis | 8/10 | 4 | BTLO 10/10, full investigation, IOC extraction, nested attachment evasion |
| Network traffic analysis | 8/10 | 3 | Wireshark PCAP work Days 1–10 — solid foundation |
| Threat detection / detection engineering | 7/10 | 4 | Sigma rules, YARA rules, both written and tested |
| Endpoint detection (EDR) | 7/10 | 1 | CrowdStrike, Carbon Black, SentinelOne — heard of them, never touched any |
| Vulnerability management | 6/10 | 1 | Know the concept, no hands-on |
| Cloud security (AWS/Azure) | 6/10 | 1 | Minimal. Know what it is, never worked in a cloud environment |
| Ticketing systems (ServiceNow, Jira) | 6/10 | 1 | Never used either in a security context |
| Elastic / KQL | 5/10 | 2 | Converted Sigma rules to KQL — haven't used Elastic directly |
| Windows administration | 5/10 | 2 | Basic — set up VMs, worked with Event Viewer and registry |
| Scripting (Python/PowerShell) | 5/10 | 1 | Know Python basics from uni — haven't applied it to security yet |
| Security+  | 5/10 | 0 | Not certified yet |
| Active Directory | 4/10 | 1 | Know what it is, never administered it or attacked/defended it |
| Threat intelligence | 4/10 | 2 | Used MITRE, read threat reports — haven't worked with feeds or platforms |
| Malware analysis | 3/10 | 2 | YARA rules touch this — haven't done static or dynamic malware analysis properly |
| Firewall / IDS / IPS | 3/10 | 1 | Conceptual knowledge only |
| Communication / report writing | 10/10 | 4 | Day 25 — wrote the same incident three ways for three audiences |
 
---

## What Kept Showing Up
 
Every single job description mentioned log analysis, SIEM experience, and MITRE ATT&CK. Those three are non-negotiable. The good news is I've touched all three.
 
The things that surprised me: EDR platforms came up in 7 out of 10 JDs. I have zero hands-on with CrowdStrike, Carbon Black, or SentinelOne. That's a real gap because a lot of SOC work in real environments is done through an EDR, not just a SIEM.
 
Cloud security came up more than I expected. 6 out of 10 JDs mentioned AWS or Azure at least once. That's not something I've planned for yet.
 
Scripting (Python or PowerShell) appeared in 5 JDs. I know Python from uni but I've never applied it to anything security-related. That's a gap I can close faster than the others.
 
---
 
## Top 5 Gaps
 
1. EDR platforms — CrowdStrike, Carbon Black, SentinelOne
2. Cloud security — AWS/Azure fundamentals
3. Scripting — Python applied to security tasks
4. Active Directory — attacks and defence
5. Security+ certification