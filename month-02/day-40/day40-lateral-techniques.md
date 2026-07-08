# Day 40 — Lateral Movement Techniques Reference

**Date:** 2026-06-21

---

## Quick Reference Table

| Technique | MITRE ID | Privileges needed | Ports | Key artifact | Event ID to watch |
|-----------|----------|------------------|-------|-------------|------------------|
| PSExec / SMB admin shares | T1021.002 | Local admin on target | TCP 445 | Service created on target | 7045 (service), 4624 type 3 |
| WMI remote execution | T1047 | Local admin on target | TCP 135 + dynamic | Process spawned by WmiPrvSE.exe | Sysmon 1 (parent = WmiPrvSE) |
| PowerShell Remoting (WinRM) | T1021.006 | Remote Mgmt Users / local admin | TCP 5985/5986 | PS Script Block logs | 4103/4104, 4624 type 3 |
| RDP | T1021.001 | Remote Desktop Users / local admin | TCP 3389 | Logon type 10 on target | 4624 type 10, 4778/4779 |
| Scheduled Task (remote) | T1053.005 | Local admin on target | TCP 445 | Task created on target | 4698, 4624 type 3 |

---

## Source vs Destination Artifacts

One thing I kept in mind while researching this: lateral movement creates artifacts on BOTH machines — the source (attacker's foothold) and the destination (target machine). Defenders who only look at one side miss half the picture.

| Technique | Source artifacts | Destination artifacts |
|-----------|-----------------|----------------------|
| PSExec | schtasks.exe / sc.exe execution, SMB outbound | New service (7045), file in ADMIN$ (Sysmon 11), logon type 3 |
| WMI | wmic.exe or PowerShell WMI call, DCOM outbound | WmiPrvSE spawning child process, logon type 3 |
| WinRM | Enter-PSSession / Invoke-Command, port 5985/5986 outbound | Logon type 3, PS Script Block logs |
| RDP | mstsc.exe execution, port 3389 outbound | Logon type 10 (4624), session events (4778) |
| Scheduled Tasks | schtasks.exe with /s flag, SMB outbound | Task created (4698), task file in System32\Tasks |

---

## Logon Types — Quick Reference

Windows logon types are critical for lateral movement detection:

| Type | Name | What it means |
|------|------|---------------|
| 2 | Interactive | Local login (keyboard at the machine) |
| 3 | Network | Remote access to shared resource (SMB, WMI, most remote tools) |
| 4 | Batch | Scheduled task |
| 5 | Service | Service startup |
| 7 | Unlock | Screen unlock |
| 10 | RemoteInteractive | RDP |
| 11 | CachedInteractive | Cached domain credentials |

For lateral movement hunting: **focus on logon types 3 and 10.** They represent remote access and are the most common types seen during lateral movement.

I cross-checked the event ID list against a Windows Security Log reference so I wasn't guessing the telemetry.

![Windows Security Log Events reference used to sanity-check the lateral movement event IDs](./screenshots/Screenshot%202026-07-08%20214838.png)

---

## What Distinguishes Admin from Attacker

This is the hardest part of lateral movement detection. Both a legitimate IT admin and an attacker might use PSExec to connect from one machine to another. The difference is:

**Legitimate admin:**
- Known admin account
- Known source machine (admin workstation or jump server)
- Known target (server they manage)
- During business hours
- Expected frequency (not connecting to 20 machines in 5 minutes)

**Attacker:**
- May use a compromised user account, not an admin account
- Source machine is an end-user workstation, not an admin station
- Connecting to machines they haven't connected to before
- May be outside business hours
- Moving fast — multiple targets in short succession (velocity anomaly)

The detection logic therefore needs to ask: is this account moving between these machines at this time at this speed? Not just: did remote access happen?

I kept the response side in mind too, because once lateral movement starts turning into a real incident, the IR question becomes bigger than the single alert.

![Mandiant cybersecurity consulting page used to keep the lateral movement work tied to real incident response context](./screenshots/Screenshot%202026-07-08%20214958.png)