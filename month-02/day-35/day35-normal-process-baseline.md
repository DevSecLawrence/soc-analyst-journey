# Day 35 — Normal Process Baseline (Windows Host)

**Date:** 2026-06-25
**Tool:** Process Hacker 2
**Machine:** Windows host (personal machine, not VM)

This is my reference for what normal Windows process trees look like. Built by opening Process Hacker on my actual machine and documenting what I saw. The point isn't to memorise every process — it's to know the normal parent-child relationships so that abnormal ones stand out.

---

## Core Windows Processes and Their Normal Parents

| Process | Normal Parent | Notes |
|---------|--------------|-------|
| `System` | None | The kernel itself — no parent |
| `smss.exe` | System | First user-mode process after boot |
| `csrss.exe` | smss.exe | Windows subsystem — one per session |
| `wininit.exe` | smss.exe | Starts services.exe, lsass.exe, lsaiso.exe |
| `services.exe` | wininit.exe | Service Control Manager — only one instance |
| `lsass.exe` | wininit.exe | Authentication — only one instance, always from wininit |
| `svchost.exe` | services.exe | Many instances — all should be from services.exe |
| `explorer.exe` | userinit.exe | Windows shell — what you see when you log in |
| `taskhostw.exe` | svchost.exe | Task host for Windows tasks |

**Rule of thumb:** If any of these have a parent that's NOT in this table — investigate immediately.

---

## What Explorer.exe Normally Spawns

Explorer.exe spawns whatever the user opens directly. Things I saw on my machine:

- `chrome.exe` — opened Chrome
- `code.exe` — opened VS Code
- `VirtualBox.exe` — opened VirtualBox
- `notepad.exe` — opened Notepad
- `explorer.exe` — opened a new File Explorer window

**Normal:** Any application the user deliberately opens.
**Suspicious:** `powershell.exe`, `cmd.exe`, `wscript.exe`, `mshta.exe` — these shouldn't appear as Explorer children from normal user activity.

---

## What svchost.exe Normally Looks Like

Multiple instances, all parented to services.exe. Each instance hosts one or more Windows services. You can right-click any svchost.exe in Process Hacker → Properties → Services tab to see which services it's hosting.

Common legitimate svchost.exe service groups I saw:
- Windows Update (`wuauserv`)
- DHCP Client (`Dhcp`)
- DNS Client (`Dnscache`)
- Windows Defender (`WinDefend`)
- Print Spooler (`Spooler`)
- Windows Search (`WSearch`)

**Key check:** Path should always be `C:\Windows\System32\svchost.exe`. Any svchost.exe from a different path = malware.

---

## Chrome's Normal Process Tree

```
chrome.exe (main process — from explorer.exe when user opens Chrome)
  ├── chrome.exe --type=gpu-process
  ├── chrome.exe --type=utility --utility-sub-type=network.mojom.NetworkService
  ├── chrome.exe --type=renderer (one per tab)
  ├── chrome.exe --type=renderer (one per tab)
  └── chrome.exe --type=extension
```

All Chrome children are chrome.exe spawning chrome.exe. The `--type` argument tells you what role each process plays. This is completely normal.

**Suspicious:** Chrome spawning anything that isn't chrome.exe — especially `cmd.exe`, `powershell.exe`, or any executable from outside Chrome's installation directory.

---

## Normal Processes at Boot (Before User Logs In)

These should be running before you even log in. If they're missing or have wrong parents, something has tampered with the boot process:

```
System
  └── smss.exe
        ├── csrss.exe (Session 0)
        ├── csrss.exe (Session 1 — user session)
        └── wininit.exe
              ├── services.exe
              │     └── svchost.exe (×many)
              └── lsass.exe
```

---

## Red Flags — Things That Should Not Exist

These combinations in a process tree mean immediate investigation:

| What you see | Why it's suspicious |
|-------------|---------------------|
| `svchost.exe` parented to anything other than `services.exe` | Malware impersonating Windows service host |
| `lsass.exe` with more than one instance | Malware impersonating LSASS |
| `WINWORD.EXE` → `cmd.exe` or `powershell.exe` | Malicious macro executing |
| `explorer.exe` → `powershell.exe` directly | Script or malware triggered from desktop |
| Any process running from `C:\Users\*\AppData\Temp\` | Malware dropped in user-writable location |
| Process name matches a system process but wrong path | Masquerading / process name spoofing |
| `mshta.exe` making outbound network connections | LOLBin abuse |