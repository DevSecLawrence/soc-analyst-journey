# Day 34 — Sysmon Event ID Reference
 
**Date:** 2026-06-25
**Source:** LetsDefend Sysmon challenge logs + Sysmon documentation
 
This is my personal reference for the Sysmon Event IDs that matter most for SOC work. Not every Event ID — just the ones that show up most in real investigations and detection use cases.
 
---
 
## Event ID 1 — Process Creation
 
**What it logs:** Every new process that starts. Includes the full command line, parent process, user account, working directory, and SHA256 hash of the executable.
 
**What makes it powerful:** The command line. Windows native process logging (Event ID 4688) can capture process creation but often doesn't capture the command line arguments by default. Sysmon always captures the full command line.
 
**Key detection use cases:**
- PowerShell with `-EncodedCommand` or `-enc` flags
- cmd.exe spawning from unusual parents (Word, Excel, browser)
- Scripts running from Temp or AppData
- Processes with suspicious hashes (match against known-bad hashes)
**Example suspicious pattern:**
```
ParentImage: C:\Program Files\Microsoft Office\Office16\WINWORD.EXE
Image: C:\Windows\System32\cmd.exe
CommandLine: cmd.exe /c powershell.exe -enc [base64]
```
Word spawning cmd spawning PowerShell with encoded command = almost certainly malicious macro.
 
---
 
## Event ID 3 — Network Connection
 
**What it logs:** Every outbound TCP/UDP connection. Includes the process making the connection, source IP/port, destination IP/port, whether it was initiated or received.
 
**What makes it powerful:** Connects network activity to the specific process that generated it. A firewall log tells you a connection happened. Sysmon Event ID 3 tells you which process on which machine made it.
 
**Key detection use cases:**
- PowerShell or cmd.exe making outbound connections (unusual — should not do this normally)
- Connections to non-standard ports (not 80/443/8080)
- Connections from processes that have no reason to make network connections (Notepad, Calculator)
- Beaconing patterns — same process connecting to the same IP repeatedly at regular intervals
**Note on noise:** Event ID 3 generates a lot of data on busy machines. Good configs filter out known-good connections (Windows Update, browser traffic) and focus on process/port combinations that are inherently suspicious.
 
---
 
## Event ID 7 — Image Loaded
 
**What it logs:** Every DLL or module loaded by any process. Includes the process loading it, the path of the DLL, and its hash.
 
**What makes it powerful:** Catches DLL injection and DLL hijacking — two techniques where malicious code hides inside legitimate processes.
 
**Key detection use cases:**
- Known-bad DLL hashes
- DLLs loaded from unusual paths (Temp, AppData, user-writable locations)
- Unsigned DLLs loaded by processes that normally only load signed ones
**Caution:** This is the noisiest Event ID. A single process loading hundreds of DLLs is normal. Most configs restrict this to unsigned DLLs or DLLs from suspicious paths only.
 
---

## Event ID 11 — File Created
 
**What it logs:** Every file written to disk. Includes the process that created it and the full path.
 
**What makes it powerful:** Catches malware dropping files — payloads, scripts, additional tools — at the moment they land on disk.
 
**Key detection use cases:**
- Executables created in Temp, AppData, or user-writable directories
- Files created by browser or email processes (phishing delivery)
- Script files (.ps1, .bat, .vbs) created in unusual locations
- Files with randomised names (common in malware)
**Example suspicious pattern:**
```
Image: C:\Program Files\Google\Chrome\Application\chrome.exe
TargetFilename: C:\Users\labuser\AppData\Local\Temp\update.exe
```
Chrome dropping an executable into Temp = immediate investigation.
 
---
 
## Event ID 13 — Registry Value Set
 
**What it logs:** Every registry value written. Includes the process that wrote it, the full registry key path, and the new value data.
 
**What makes it powerful:** Catches persistence mechanisms at the moment they're established, not after the next reboot.
 
**Key detection use cases:**
- Writes to Run/RunOnce keys (`HKCU\Software\Microsoft\Windows\CurrentVersion\Run`)
- Writes to services registry keys
- Modifications to security policy keys
- Any registry write by a process that has no reason to touch the registry
**MITRE ATT&CK:** T1547.001 — Boot or Logon Autostart Execution: Registry Run Keys
 
---

