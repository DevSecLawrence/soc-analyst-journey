# Day 39 — Credential Theft Techniques: How Attackers Steal the Keys
 
**Date:** 2026-07-07
 
---
 
## Why Credentials Are the Real Target
 
Credentials are what let attackers stop hacking and start logging in. Once someone has valid credentials — especially a domain admin account — they don't need exploits anymore. They just authenticate normally like any other user and the environment treats them as legitimate. That's why credential theft sits right in the middle of almost every serious breach.
 
The analogy I keep coming back to: breaking into a building is hard. Stealing someone's key and making a copy is much easier — and way harder to detect because the door opens normally.
 
---
 
## Technique 1 — LSASS Memory Dumping
 
**MITRE:** T1003.001
 
**How it works:**
LSASS (Local Security Authority Subsystem Service) is a Windows process that handles authentication. When you log into Windows, LSASS stores your credentials in memory — including hashed passwords and in some configurations plaintext passwords — so it doesn't have to ask you to re-authenticate for every action.
 
Attackers dump this memory to extract those credentials. The most well-known tool for this is Mimikatz, which can extract credentials from LSASS memory with a single command:
```
sekurlsa::logonpasswords
```
 
This gives the attacker every set of credentials currently loaded in memory on that machine — which on a domain controller could mean every active session in the entire organization.
 
**What telemetry reveals it:**
- **Sysmon Event ID 10** — Process Access. LSASS being accessed by an unexpected process is the key signal. `lsass.exe` being read by `cmd.exe` or `powershell.exe` is not normal.
- Look for: `GrantedAccess` value of `0x1010` or `0x1410` — these access rights are what Mimikatz requests
- The accessing process running from a temp directory or having no digital signature
**Protections:**
- **LSASS as Protected Process Light (PPL)** — makes LSASS harder to access from userland processes. Requires a signed driver to bypass.
- **Credential Guard** — moves credential storage into a virtualization-based isolated container that even admin processes can't access directly
- **Removing WDigest** — in older Windows versions, WDigest stored plaintext passwords in LSASS. Disabling it removes plaintext creds from memory.
---
 
## Technique 2 — SAM Database Extraction
 
**MITRE:** T1003.002
 
**How it works:**
The SAM (Security Account Manager) database stores local Windows account password hashes. It lives at `C:\Windows\System32\config\SAM` but Windows locks it while running — you can't just copy it while the OS is active.
 
Attackers get around this using Volume Shadow Copies (VSS) — backup snapshots Windows creates automatically. The SAM in a shadow copy isn't locked, so:
```
vssadmin list shadows
copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\System32\config\SAM C:\Temp\SAM
```
