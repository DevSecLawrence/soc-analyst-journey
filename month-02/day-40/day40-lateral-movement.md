# Day 40 — Lateral Movement Detection

**Date:** 2026-06-21
**MITRE Tactic:** TA0008 — Lateral Movement
**Lab status:** Windows VM still down — research and detection writing only. Hands-on pending lab rebuild.

---

## Why Lateral Movement Matters

Getting into a network is only the first step for an attacker. The machine they land on is rarely the one with what they actually want — credentials, sensitive data, domain controllers. Lateral movement is how they get from the entry point to the target.

This is also where defenders have one of the best chances to catch an attack in progress. The initial compromise might be fast and quiet. But movement between machines generates telemetry — authentication events, network connections, service installations. An attacker who moves laterally is making noise across multiple systems simultaneously, which means the SIEM can correlate it in a way it can't for a single endpoint compromise.

The hard part: every technique used for lateral movement is also a legitimate admin tool. PSExec, WMI, WinRM, RDP — IT teams use all of these daily. Detection is about context and anomaly, not the tool itself.

---

## The 5 Techniques

### 1. PSExec / SMB Admin Shares (T1021.002)

**How it works:**
PSExec connects to the target machine's admin share (`\\target\ADMIN$` or `\\target\C$`), copies a service binary, installs it as a Windows service, and executes it. The service runs the attacker's command and returns output.

**Required privileges:** Local administrator on the target machine minimum. Domain admin is common.

**Ports used:** TCP 445 (SMB)

**Artifacts created:**
- Service installation on target (Windows Event ID 7045 — new service created)
- File copy to `ADMIN$` share (Sysmon Event ID 11 — file created)
- Network logon event on target (Windows Event ID 4624 — logon type 3)
- Named pipe connection

**Detection opportunities:**
- Event ID 7045 on target for a short-lived service with a random name
- Event ID 4624 logon type 3 (network logon) from an unusual source IP
- SMB connections to admin shares from workstations (workstation to workstation SMB is unusual — should be server to workstation)

**Legitimate vs suspicious:**
Legitimate IT admin use of PSExec is common. The difference: legitimate use follows a pattern (same admin account, same source machine, during business hours, against servers). Attacker use follows a different pattern (new source, new account, multiple targets in short succession, unusual hours).

---

### 2. WMI Remote Execution (T1047)

**How it works:**
WMI (Windows Management Instrumentation) has remote execution capability via DCOM. An attacker runs a command on a remote machine through WMI without needing to copy any files — the command runs in memory via the WMI service already running on the target.

**Required privileges:** Local administrator on the target.

**Ports used:** TCP 135 (DCOM/RPC endpoint mapper) + dynamic high ports

**Artifacts created:**
- WMI activity logged if Sysmon is configured for it (Sysmon Event IDs 19-21)
- Process creation on target spawned by `WmiPrvSE.exe` (Sysmon Event ID 1 — parent process is WmiPrvSE)
- Network logon on target (Event ID 4624 logon type 3)

**Detection opportunities:**
- Any process spawned by `WmiPrvSE.exe` running cmd.exe, PowerShell, or anything unusual
- Remote WMI connections from workstations to servers (or workstation to workstation)
- WMI activity outside of normal admin windows

**Why it's stealthy:**
WMI is a built-in Windows service that's always running. It generates minimal default logging. Without Sysmon configured specifically to log WMI events, many environments are completely blind to WMI-based lateral movement.

---

### 3. PowerShell Remoting / WinRM (T1021.006)

**How it works:**
Windows Remote Management (WinRM) is the Microsoft protocol for remote PowerShell sessions. An attacker runs `Enter-PSSession` or `Invoke-Command` to execute PowerShell on a remote machine, essentially getting an interactive or command shell.

**Required privileges:** Remote Management Users group membership or local admin.

**Ports used:** TCP 5985 (HTTP) or TCP 5986 (HTTPS)

**Artifacts created:**
- Windows Event ID 4624 logon type 3 on target
- PowerShell operational log (Event ID 4103/4104) if Script Block Logging is enabled
- Network connection on ports 5985/5986
- Sysmon Event ID 3 (network connection) for the WinRM traffic

**Detection opportunities:**
- WinRM connections from unusual source machines
- PowerShell Script Block Logging — captures the actual commands run remotely
- Interactive sessions (Enter-PSSession) from non-admin workstations

**The visibility gap:**
WinRM over HTTPS (port 5986) encrypts the payload. Network inspection won't show the commands. Host-based logging (PowerShell Script Block Logging, Sysmon) is essential here because network monitoring alone misses the content.

---

### 4. RDP (T1021.001)

**How it works:**
Remote Desktop Protocol allows interactive graphical sessions on remote machines. An attacker with valid credentials RDPs in and controls the machine as if they're sitting at it.

**Required privileges:** Remote Desktop Users group membership or local admin.

**Ports used:** TCP 3389

**Artifacts created:**
- Windows Event ID 4624 logon type 10 (RemoteInteractive) on target
- Windows Event ID 4778/4779 — session connected/disconnected
- Sysmon Event ID 3 — network connection to port 3389
- Process creation for mstsc.exe on the source machine

**Detection opportunities:**
- RDP from unexpected sources (employee workstation to domain controller)
- RDP at unusual times (middle of the night)
- RDP to multiple machines in short succession (same account, multiple destinations)
- Event ID 4624 logon type 10 from external IPs (if RDP is internet-facing — which it shouldn't be)

**Why it's dangerous to miss:**
RDP gives the attacker a fully interactive session — they can do anything a logged-in user can do. It's also one of the most commonly abused techniques in ransomware incidents because it's fast and gives full control.

---

### 5. Scheduled Task Remote Creation (T1053.005)

**How it works:**
Windows allows creating scheduled tasks on remote machines via `schtasks /create /s TARGETMACHINE`. An attacker uses this to execute their payload on a remote system at a specified time or trigger.

**Required privileges:** Local administrator on target.

**Ports used:** TCP 445 (SMB) for the RPC call

**Artifacts created:**
- Windows Event ID 4698 on target — scheduled task created
- Windows Event ID 4624 logon type 3 on target — network logon
- Task XML written to `C:\Windows\System32\Tasks\` on target (Sysmon Event ID 11)
- Process creation for schtasks.exe on source (Sysmon Event ID 1)

**Detection opportunities:**
- Event ID 4698 with the creator being a remote machine (check the SubjectUserName and source IP)
- Scheduled tasks created outside of business hours
- Tasks pointing to files in user-writable directories
- Tasks with action fields containing base64 or obfuscated commands

---

## The Key Pattern Across All 5

Every technique creates a network logon event (4624 logon type 3) on the target machine. That single event, correlated with what happened before it and after it, is often the thread that unravels lateral movement.

The challenge is volume — in a large environment, logon type 3 events happen thousands of times per day for completely legitimate reasons. The signal is in the anomaly:
- Same account, many destinations, short time window
- Source machine that doesn't normally connect to the target
- Activity outside of normal hours for that account
- Connection immediately followed by service creation, task creation, or process execution

None of those patterns are visible on any single machine's logs. This is why SIEM correlation across the full environment matters so much for lateral movement specifically.

---

## What I Concluded

Lateral movement is the attacker at their most detectable — and most dangerous. They're making noise across multiple systems. They're touching authentication infrastructure. They're creating services and tasks. But the noise only becomes a signal if you're correlating it across systems rather than looking at each machine in isolation.

The other thing that clicked today: "admin tools used maliciously" is the core problem in lateral movement detection. There's no malware to signature-match, no exploit to detect. A legitimate copy of PsExec doing malicious things looks exactly like a legitimate copy of PsExec doing legitimate things. The only way to tell the difference is context — who is using it, from where, to where, and when.

---

## Assumption I Made

I assumed that lateral movement would be easy to detect because it involves multiple systems. The reality is the opposite — it's harder to detect precisely because it spans multiple systems. Each individual event looks legitimate. The attack only becomes visible when you stitch events across systems together, and that requires either a well-tuned SIEM with proper correlation rules or an analyst actively hunting rather than waiting for alerts.

---

## Uncertainty I Have

I don't know how to baseline normal admin movement patterns in practice. The detection logic for lateral movement depends heavily on knowing what "normal" looks like for that environment — which accounts normally RDP to which machines, which source IPs normally make SMB connections to which servers. Without that baseline, almost every detection rule will either miss real attacks or drown in false positives. Building that baseline is a weeks-long process in a real environment and I don't have a framework yet for how to do it systematically.