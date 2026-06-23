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

