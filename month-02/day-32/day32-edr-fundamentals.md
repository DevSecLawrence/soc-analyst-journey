# Day 32 — EDR Fundamentals: Understanding Endpoint Detection
 
**Date:** 2026-06-14
 
---
 
## What I Did
 
Spent today researching EDR platforms — what they actually are, how they work, and why they matter. This came up in 7 out of 10 job descriptions I looked at on Day 28 and I had zero hands-on knowledge of any of them. Today was about fixing the conceptual gap before touching any actual tool.
 
Researched 3 platforms: CrowdStrike Falcon, Microsoft Defender for Endpoint, and Carbon Black.
 
---
 
## What is EDR
 
Before today I thought EDR was just "antivirus but better." It's not. Antivirus looks for known bad signatures — it matches files against a list of known malware. EDR watches behaviour — it records everything a process does and flags it when the behaviour looks suspicious, even if the file itself has never been seen before.
 
The way I think about it now: antivirus is like a bouncer checking IDs at the door. EDR is a CCTV system that watches everything happening inside the building and can kick someone out mid-conversation if they start acting suspiciously.
 
---

## The 3 Platforms
 
### CrowdStrike Falcon
 
**What telemetry it collects:**
Process creation and execution, parent-child process relationships, network connections, file system changes, registry modifications, user logon events, and memory activity.
 
**How detection works:**
Three layers — signature matching for known malware, behavioural analysis that looks at what a process is doing rather than what it is, and machine learning that flags things that don't match normal patterns even if they don't match any known attack either.
 
**Response actions available:**
Network isolation (cut the machine off from everything else while keeping it manageable), process kill, file quarantine, and remote shell access for investigation.
 
**SIEM integration:**
Sends alerts and telemetry to a SIEM via API or syslog. In practice this means your CrowdStrike alerts end up in Splunk or Elastic alongside your network and authentication logs so you can correlate across everything.
 
---

