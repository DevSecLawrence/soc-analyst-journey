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
Then they extract password hashes offline using tools like `secretsdump.py` from Impacket.
 
**What telemetry reveals it:**
- **Sysmon Event ID 1** — Process creation showing `vssadmin.exe` being run by an unexpected process
- **Windows Event ID 8222** — Shadow copy created
- File access to the SAM file from a non-system process
- `reg save HKLM\SAM` command in process creation logs — another way to extract SAM
**Protections:**
- Restrict access to `vssadmin.exe` via application control
- Monitor shadow copy creation and deletion (attackers also delete shadows to prevent recovery)
- Ensure local admin accounts use unique passwords per machine (LAPS)
---
 
## Technique 3 — Credential Manager Access
 
**MITRE:** T1555.004
 
**How it works:**
Windows Credential Manager stores saved passwords — things like saved network credentials, RDP passwords, and in some cases browser credentials. Attackers can dump these using built-in Windows tools:
```
cmdkey /list
```
Or via PowerShell:
```powershell
[Windows.Security.Credentials.PasswordVault,Windows.Security.Credentials,ContentType=WindowsRuntime]::new().RetrieveAll()
```
 
**What telemetry reveals it:**
- **Sysmon Event ID 1** — `cmdkey.exe` execution, especially if run by an unexpected parent process
- PowerShell reading Credential Manager via API — visible in Script Block Logging (Event ID 4104)
- Access to `%APPDATA%\Microsoft\Credentials\` directory
**Protections:**
- Don't save credentials in Credential Manager for privileged accounts
- Monitor Credential Manager access via PowerShell Script Block Logging
- Use a proper PAM (Privileged Access Management) solution for privileged credentials
---
 
## Technique 4 — Kerberos Ticket Extraction (Kerberoasting)
 
**MITRE:** T1558.003
 
**How it works:**
Kerberos is the authentication protocol used in Active Directory environments. When you authenticate to a service (like a file share or database), Windows requests a Kerberos service ticket encrypted with the service account's password hash.
 
Kerberoasting exploits this: any authenticated domain user can request service tickets for any service principal name (SPN). The attacker requests a ticket, takes it offline, and brute-forces the service account's password from the ticket's encryption.
 
This is effective because service accounts often have weak passwords, don't expire, and have high privileges.
 
**What telemetry reveals it:**
- **Windows Event ID 4769** — Kerberos Service Ticket Requested. Look for: `TicketEncryptionType = 0x17` (RC4 encryption — what Kerberoasting uses), multiple tickets requested in a short time, tickets requested for accounts that don't normally have Kerberos activity
- **Event ID 4768** — Kerberos Ticket Granting Ticket (TGT) requested
**Protections:**
- Use AES encryption for Kerberos instead of RC4 (makes offline cracking much harder)
- Enforce strong passwords on all service accounts (25+ characters)
- Use Group Managed Service Accounts (gMSA) — Windows manages the passwords automatically and they rotate regularly
- Monitor for unusual Kerberos ticket requests in volume or targeting
---

## Technique 5 — Browser Credential Theft
 
**MITRE:** T1555.003
 
**How it works:**
Modern browsers (Chrome, Edge, Firefox) save passwords locally — and they're encrypted using Windows DPAPI (Data Protection API), which ties the encryption to the current user's account. Any process running as that user can decrypt them.
 
Chrome stores passwords in:
```
%LOCALAPPDATA%\Google\Chrome\User Data\Default\Login Data
```
 
This is an SQLite database. While Chrome is closed, any process can read and decrypt it using the user's DPAPI key. Tools like `LaZagne` automate this across multiple browsers simultaneously.
 
**What telemetry reveals it:**
- **Sysmon Event ID 1** — Unexpected process accessing Chrome's `Login Data` file
- **Sysmon Event ID 11** — File creation in browser profile directories (attacker copying the database)
- DPAPI decryption calls from unexpected processes (visible in some EDR telemetry)
**Protections:**
- Don't save passwords in browsers for privileged accounts — use a password manager
- EDR behavioral detection for unexpected DPAPI access
- Monitor for SQLite access to browser profile directories from non-browser processes
---
 
## Event IDs Summary
 
| Event ID | Source | What it catches |
|----------|--------|-----------------|
| Sysmon 10 | Sysmon | LSASS process access |
| Sysmon 1 | Sysmon | Suspicious process execution (mimikatz, vssadmin, cmdkey) |
| 4624 | Windows Security | Successful logon |
| 4625 | Windows Security | Failed logon |
| 4768 | Windows Security | Kerberos TGT requested |
| 4769 | Windows Security | Kerberos service ticket requested — key for Kerberoasting |
| 4771 | Windows Security | Kerberos pre-auth failed |
| 4104 | PowerShell | Script block logging — catches PowerShell credential access |
| 8222 | VSS | Shadow copy created |
