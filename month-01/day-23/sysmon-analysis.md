

raw
Day23 sysmon analysis · MD
# Day 23 — Building the Detection Lab: Sysmon Log Analysis
 
**Date:** 2026-06-07
**Platform:** LetsDefend — Log Analysis With Sysmon challenge
**Lab:** Browser-based Windows machine (VNC via vnc.letsdefend.io)
 
---
 
## Why I Did It This Way
 
Original plan was to build a local detection lab — Windows 10 VM on VirtualBox, isolated host-only network, Sysmon installed manually. Got most of the way through it but hit a storage setback (accidentally formatted the external drive the VM was on). 
 
Rather than sit on an incomplete day, I moved to LetsDefend's browser-based lab. Same concepts — Sysmon logs, Event Viewer, real attack investigation — just without the infrastructure setup. I'll rebuild the local lab when storage is sorted.
 
---

## Environment
 
- **Lab type:** Browser-based Windows VM via LetsDefend VNC
- **Challenge:** Log Analysis With Sysmon (`app.letsdefend.io/challenge/log-analysis-with-sysmon`)
- **Log file:** `C:\Users\LetsDefend\Desktop\ChallengeFile\Sysmon_chall.zip`
- **Total events:** 757 Sysmon events
- **Log date range:** 3/13/2024
---

## Setup Inside the Lab
 
1. Connected to the LetsDefend Windows machine via browser VNC
2. Opened the ChallengeFile folder on the Desktop
3. Extracted `Sysmon_chall.zip`
4. Opened Event Viewer → File → Open Saved Log → loaded the `.evtx` file
5. Log appeared under Saved Logs → Sysmon with 757 events ready to analyse
---
 
 ## Investigation
 
### Finding Initial Access — Event ID 1 (Process Creation)
 
Filtered Event Viewer by Event ID 1 to look at all process creation events. Scrolled through looking for anything that didn't belong — specifically processes being spawned by a parent that made no sense.
 
**Finding:** `IDM.exe` — Internet Download Manager — was the file that gave the attacker initial access. A download manager spawning shells is an immediate red flag. Legitimate download managers don't do that.
 
✅ Confirmed correct on the challenge.
 
---

