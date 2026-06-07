

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

### Finding the UAC Bypass — Event ID 1 (Process Creation)
 
Kept the Event ID 1 filter running and searched for `fodhelper`. Found it:
 
```
Image:         C:\Windows\System32\fodhelper.exe
Description:   Features On Demand Helper
FileVersion:   10.0.19041.1 (WinBuild.160101.0800)
ParentImage:   C:\Windows\explorer.exe
ParentUser:    DESKTOP-0V6VB41\Gabr
IntegrityLevel: (visible in earlier entry — Medium on parent, escalates via fodhelper)
```
 
**Finding:** `fodhelper.exe` was used to bypass UAC. This is a well documented technique — fodhelper is a trusted Windows binary that auto-elevates without triggering a UAC prompt. Attackers write a malicious command to `HKCU\Software\Classes\ms-settings\shell\open\command` and when fodhelper runs it executes that command at High integrity.
 
**MITRE ATT&CK:** T1548.002 — Abuse Elevation Control Mechanism: Bypass User Account Control
 
---
 
 ### Persistence — Registry Run Key
 
Found registry modification at:
```
HKCU\Software\Microsoft\Windows\CurrentVersion\Run
```
 
This is a classic persistence mechanism — anything written here executes automatically when the user logs in. The attacker used this to make sure their tooling survived a reboot.
 
**MITRE ATT&CK:** T1547.001 — Boot or Logon Autostart Execution: Registry Run Keys
 
---

## What I Didn't Get To
 
Free lab access ended before I could complete:
- The dropped file location (Event ID 11)
- The technique name and ID for the dropped EXE
- The name of the attack
- The EXE run under elevated privileges
- The downloaded file name
Will revisit this challenge when I have VIP access or find an equivalent lab with the same Sysmon evtx file to finish the investigation.
 
---
 
## What I Concluded
 
Sysmon adds a completely different layer on top of standard Windows Event Logs. Native Windows logs tell you something happened — a process started, a user logged in. Sysmon tells you the full context — the parent process, the command line, the hash, the integrity level, the network connection it made. Without Sysmon you'd see `cmd.exe` started. With Sysmon you see `IDM.exe` spawned `cmd.exe` with a suspicious command line at Medium integrity, which then triggered `fodhelper.exe` to escalate to High. That's the difference between noise and an actual investigation trail.
 
The parent/child process relationship is everything. That's what turns a list of process names into an attack timeline.
 
---

## Assumption I Made
 
I assumed UAC bypass techniques were rare or complex. `fodhelper.exe` is a built-in Windows binary — it's been on every Windows 10 machine since day one. Attackers don't need to bring exotic tools when the OS itself has trusted binaries that auto-elevate. That was a gap in how I was thinking about living-off-the-land attacks.
 
---

## Uncertainty I Have
 
I don't fully understand yet how to tune Sysmon config to reduce noise without missing things. 757 events from what looks like a short attack window is a lot to scroll through manually. In a real environment that'd be tens of thousands of events a day. I need to understand how the SwiftOnSecurity config filters events and where the tradeoffs are — what it logs by default vs what it ignores and why.
 
---
 
## Files
- [day23-lab-setup.md](./day23-lab-setup.md) — local VM setup attempt (partial)
- [day23-sysmon-analysis.md](./day23-sysmon-analysis.md) — this file
 