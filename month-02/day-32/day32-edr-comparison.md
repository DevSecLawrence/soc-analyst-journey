# Day 32 — EDR Platform Comparison
 
**Date:** 2026-06-14
**Platforms:** CrowdStrike Falcon, Microsoft Defender for Endpoint, Carbon Black
 
---
 
## Side by Side
 
| Feature | CrowdStrike Falcon | Microsoft Defender for Endpoint | Carbon Black |
|---------|-------------------|--------------------------------|--------------|
| Telemetry | Process, network, file, registry, memory | Process, file, registry, network, Office app behaviour | Continuous full process recording |
| Detection method | Signatures + behaviour + ML | Behaviour + Microsoft threat intel | Behaviour + retrospective analysis |
| Response actions | Isolate, kill process, quarantine, remote shell | Isolate, quarantine, restrict apps, live response | Process ban, live response, isolate |
| SIEM integration | API / syslog to any SIEM | Native to Microsoft Sentinel, API to others | API to major SIEMs |
| Standout feature | ML detection across billions of global endpoints | Tight Microsoft ecosystem integration | Full historical recording — replay any incident |
| Best for | Enterprise, cloud-first organisations | Microsoft-heavy environments (Azure, M365) | Organisations that need deep forensic capability |
 
---

## What Stands Out About Each
 
**CrowdStrike** — the market leader for a reason. The machine learning is trained on data from a huge number of endpoints globally which means it's seen more attack patterns than any other platform. The "threat graph" (how it visualises process relationships) is genuinely useful for investigation — you can see the full chain of what spawned what at a glance.
 
**Microsoft Defender for Endpoint** — if your organisation runs on Microsoft everything, this makes the most sense. It integrates with Azure AD, Microsoft Sentinel, and Microsoft 365 natively. The attack surface reduction rules are genuinely useful for hardening. And since most enterprise environments are Microsoft-heavy, this is the one a junior SOC analyst is most likely to encounter in a real job.
 
**Carbon Black** — the continuous recording is the differentiator. Most EDRs tell you what happened when they detected something. Carbon Black tells you everything that happened before and after. For incident response and forensics this is extremely powerful. The tradeoff is storage and cost.
 
---

## Which One Will I See in a Junior SOC Role?
 
Realistically — Microsoft Defender for Endpoint is the most common in mid-size enterprises. CrowdStrike is dominant in larger organisations and tech companies. Carbon Black shows up in organisations with mature security programs that prioritise forensics. As a junior analyst, MDE is probably the most important to get comfortable with first.