# Day 42 — Hunt Hypotheses
 
**Date:** 2026-06-23
**Environment:** Windows 10 endpoint + Kali Linux (local lab — VM currently down, queries pending rebuild)
 
---
 
## How to Read This Document
 
Each hypothesis follows the same structure:
- **Hypothesis** — the question being asked
- **Why it matters** — what real attack technique this covers
- **Data source** — where to look
- **Query approach** — what to search for
- **Success criteria** — what a positive finding looks like
- **False positive risk** — what legitimate activity might look the same
---
 
## Hypothesis 1 — Persistence via Scheduled Tasks Created Outside Business Hours
 
**Hypothesis:**
An attacker has established persistence by creating scheduled tasks outside of normal business hours, pointing to files in unusual locations.
 
**Why it matters:**
Scheduled tasks are a top persistence mechanism. Legitimate tasks are almost always created during business hours by known admin accounts or software installers. Tasks created at 2am by a standard user account are suspicious.
 
**Data source:**
Windows Security Event Log — Event ID 4698 (Scheduled Task Created)
 
**Query approach (Splunk SPL):**
```spl
index=windows EventCode=4698
| eval hour=strftime(_time, "%H")
| where hour < 6 OR hour > 22
| table _time, TaskName, SubjectUserName, TaskContent
| sort -_time
```
 
**Success criteria:**
Any Event ID 4698 outside 06:00–22:00 from a non-admin account or pointing to a file in `%TEMP%`, `%APPDATA%`, or `C:\Users\Public`.
 
**False positive risk:**
Legitimate backup software or scheduled maintenance tasks running overnight. Filter by known admin accounts and known task names to reduce noise.
 
---
## Hypothesis 2 — PowerShell Used for Reconnaissance
 
**Hypothesis:**
An attacker is using PowerShell to enumerate the environment — running discovery commands like `Get-ADUser`, `net user`, `ipconfig`, `whoami` — shortly after initial access or lateral movement.
 
**Why it matters:**
Post-compromise reconnaissance almost always involves PowerShell on Windows. The commands are distinctive — they're things normal users never run, but attackers run within minutes of landing on a machine.
 
**Data source:**
PowerShell Script Block Logging — Event ID 4104
Sysmon Event ID 1 — Process creation with CommandLine
 
**Query approach (Splunk SPL):**
```spl
index=sysmon EventCode=1 Image="*\\powershell.exe"
| where CommandLine LIKE "%Get-ADUser%" 
    OR CommandLine LIKE "%net user%" 
    OR CommandLine LIKE "%whoami%"
    OR CommandLine LIKE "%ipconfig%"
    OR CommandLine LIKE "%Get-NetIPAddress%"
| table _time, ComputerName, User, CommandLine, ParentCommandLine
| sort -_time
```
 
**Success criteria:**
PowerShell running enumeration commands from a non-admin account, or from an admin account on a machine they don't normally administrate.
 
**False positive risk:**
IT admin scripts, software inventory tools, and monitoring agents. The key filter is context — which account ran it and from which machine.
 
---
 
## Hypothesis 3 — Lateral Movement via WMI Remote Execution
 
**Hypothesis:**
An attacker is moving between machines using WMI remote execution — spawning processes on remote machines via the WMI service.
 
**Why it matters:**
WMI-based lateral movement is stealthy. It doesn't install a service (no Event ID 7045), it doesn't use RDP (no logon type 10). The only reliable indicator is a process being spawned with `WmiPrvSE.exe` as the parent on the destination machine.
 
**Data source:**
Sysmon Event ID 1 — Process creation
 
**Query approach (Splunk SPL):**
```spl
index=sysmon EventCode=1 ParentImage="*\\WmiPrvSE.exe"
| where Image LIKE "%cmd.exe%" 
    OR Image LIKE "%powershell.exe%"
    OR Image LIKE "%wscript.exe%"
| table _time, ComputerName, User, Image, CommandLine, ParentImage
| sort -_time
```
 
**Success criteria:**
Any shell or scripting process (`cmd.exe`, `powershell.exe`) spawned with `WmiPrvSE.exe` as the parent, especially on machines that don't normally run WMI-initiated processes.
 
**False positive risk:**
Some management tools (SCCM, antivirus) use WMI to spawn processes legitimately. Filter by known management tool process names.
 
---
## Hypothesis 4 — Data Staged for Exfiltration
 
**Hypothesis:**
An attacker is staging data for exfiltration — compressing or copying files to an unusual location before moving them out of the network.
 
**Why it matters:**
Attackers rarely exfiltrate directly from the original file locations. They typically compress data (zip, rar, 7zip) and stage it in a temporary location first. This compression step is detectable before the actual exfiltration happens.
 
**Data source:**
Sysmon Event ID 1 — Process creation (compression tools being run)
Sysmon Event ID 11 — File creation (compressed archives appearing in unusual locations)
 
**Query approach (Splunk SPL):**
```spl
index=sysmon EventCode=1
| where (Image LIKE "%7z.exe%" OR Image LIKE "%rar.exe%" OR Image LIKE "%zip%")
    AND (CommandLine LIKE "%C:\\Users\\Public%"
    OR CommandLine LIKE "%\\Temp\\%"
    OR CommandLine LIKE "%\\AppData\\%")
| table _time, ComputerName, User, Image, CommandLine
| sort -_time
```
 
**Success criteria:**
Compression tools creating archives in user-writable temporary directories, especially involving directories containing sensitive file types (`.docx`, `.xlsx`, `.pdf`, source code).
 
**False positive risk:**
Legitimate use of compression tools for backups or file transfers. Filter by destination path — legitimate backups typically go to known backup destinations, not `%TEMP%`.
 
---
