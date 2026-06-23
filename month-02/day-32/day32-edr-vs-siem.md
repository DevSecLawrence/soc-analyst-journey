# Day 32 — EDR vs SIEM: What Each Sees and Why You Need Both
 
**Date:** 2026-06-14
 
---
 
## The Simple Version
 
**EDR** = deep visibility on one endpoint. Watches processes, memory, files, registry.
 
**SIEM** = wide visibility across all infrastructure. Watches network, authentication, logs from every system.
 
Neither sees everything. Together they cover most of what matters.
 
---
 
## What EDR Catches That SIEM Misses
 
- **Fileless malware** — runs entirely in memory, never writes to disk. No file for SIEM to log, no network traffic to alert on. EDR catches the suspicious process behaviour.
- **Process injection** — one process injecting code into another (e.g. malware hiding inside explorer.exe). SIEM only sees network events — it has no visibility into what's happening inside a process.
- **Malicious scripts running locally** — PowerShell or cmd.exe running a malicious command locally generates no network traffic. EDR captures the command line arguments.
- **File system changes** — malware dropping files, modifying executables, or tampering with system binaries. SIEM doesn't watch the file system.
- **Registry persistence** — a malicious value written to a registry run key. SIEM doesn't see registry changes unless you've specifically forwarded that telemetry.
---

## What SIEM Catches That EDR Misses
 
- **Lateral movement between machines** — an attacker moving from one machine to another shows up as authentication events across multiple systems. EDR on each individual machine only sees its own activity, not the pattern across machines.
- **Pass the Hash / Pass the Ticket** — credential-based attacks that use valid authentication tokens. The endpoint looks normal. The SIEM sees the same account authenticating in two places simultaneously with no password prompt.
- **Network-level C2 traffic** — command and control communication over the network shows up in firewall and proxy logs. If the malware is careful about how it behaves on the endpoint, EDR may not flag it — but the network traffic is visible in SIEM.
- **VPN anomalies** — impossible travel (someone logging in from Nigeria and the UK within 30 minutes). Pure network/authentication data, nothing to do with endpoint behaviour.
- **Cross-system correlation** — a user running whoami on Machine A, then accessing a file share on Machine B, then creating a new account on Machine C. Each event looks minor in isolation. SIEM correlates them into a full picture.
---

## How They Complement Each Other
 
The way I think about it: EDR is the microscope, SIEM is the map.
 
EDR zooms in on one endpoint and shows you everything happening at a granular level — process by process, memory region by memory region. SIEM zooms out and shows you the entire environment — how events across dozens of machines relate to each other.
 
A real attack almost always touches both layers. The initial compromise might be endpoint-level (malware executing on one machine, caught by EDR). The subsequent lateral movement is network-level (authentication events across machines, caught by SIEM). You need both to see the full attack.
 
---

## 5 ATT&CK Techniques Mapped to Detection Source
 
| Technique | ID | Best detected by | Why |
|-----------|-----|-----------------|-----|
| PowerShell with encoded commands | T1059.001 | EDR | Process creation with command line arguments — endpoint level, may not generate network traffic |
| Pass the Hash | T1550.002 | SIEM | Authentication event anomaly — same account, no password, multiple machines |
| Process injection | T1055 | EDR | Memory-level activity inside a process — invisible to network logs |
| Lateral movement via SMB | T1021.002 | SIEM | Network authentication across machines — pattern only visible at infrastructure level |
| Registry run key persistence | T1547.001 | EDR | Registry write event on the endpoint — SIEM won't see this unless registry telemetry is specifically forwarded |
 
---

## In What Scenarios Would You Use Each as Primary?
 
**Use EDR as primary when:**
- Investigating a suspected malware infection on a specific machine
- Hunting for fileless or memory-based attacks
- Responding to an endpoint alert and tracing the full execution chain
- Looking for persistence mechanisms on a compromised host
**Use SIEM as primary when:**
- Investigating suspicious authentication patterns across multiple systems
- Hunting for lateral movement
- Correlating events across different data sources (network, auth, endpoint)
- Looking for C2 communication patterns in network logs
- Investigating an alert that spans more than one machine