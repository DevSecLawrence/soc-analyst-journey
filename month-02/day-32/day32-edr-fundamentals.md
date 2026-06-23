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

### Microsoft Defender for Endpoint (MDE)
 
**What telemetry it collects:**
Process execution, file changes, registry changes, network connections, user activity, and behavioural signals from Office applications (so it can catch things like Word spawning PowerShell).
 
**How detection works:**
Behaviour-based detection using Microsoft's threat intelligence from billions of endpoints globally. It also has an "attack surface reduction" layer that blocks known dangerous behaviours before they even get flagged as alerts.
 
**Response actions available:**
Device isolation, file quarantine, run antivirus scan, restrict app execution, live response (basically a remote terminal to the machine).
 
**SIEM integration:**
Native integration with Microsoft Sentinel. Can also stream to third-party SIEMs. Since Microsoft owns both the EDR and the SIEM in this case, the integration is tighter than most.
 
---

### Carbon Black (VMware)
 
**What telemetry it collects:**
Continuous recording of process activity — every process that runs, every file it touches, every network connection it makes. Unlike the others it keeps a full historical record rather than just alerting on suspicious events.
 
**How detection works:**
The continuous recording means you can go back in time and replay exactly what happened before and after an alert. Detection is behaviour-based but the differentiator is the retrospective investigation capability.
 
**Response actions available:**
Process ban (block a specific hash from ever running again), live response, network isolation.
 
**SIEM integration:**
API-based integration with major SIEMs. The continuous recording data can be queried directly or forwarded.
 
---

## What I Concluded
 
EDR and SIEM are not the same thing and one doesn't replace the other. I went into this thinking EDR was just a more advanced version of what a SIEM does. It's not — they see completely different things.
 
EDR lives on the endpoint. It watches what processes do, how they behave, what they touch in memory and on disk. It sees things that never generate a network log — a process injecting into another process, a registry key being written silently, a file being dropped and immediately executed.
 
SIEM lives on the network and across infrastructure. It sees authentication events, network flows, VPN connections, firewall logs. It correlates across many machines simultaneously.
 
A piece of malware running on one endpoint might not generate any network traffic at all. SIEM misses it completely. EDR catches it. A pass-the-hash attack moving between machines laterally might not touch the endpoint in a way EDR would flag — but the authentication logs in the SIEM show an account being used in two places simultaneously with no password prompt. EDR misses it. SIEM catches it.
 
You need both. That's the actual answer.
 
---

