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

