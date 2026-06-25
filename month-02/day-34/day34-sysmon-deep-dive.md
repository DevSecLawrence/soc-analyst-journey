# Day 34 — Sysmon Deep Dive: The Free EDR Telemetry Source
 
**Date:** 2026-06-25
**Platform:** LetsDefend — Log Analysis With Sysmon challenge + SwiftOnSecurity / Olaf Hartong config research
**Lab status:** Windows VM still down — config written from research, untested pending lab rebuild
 
---
 
## What I Did
 
Two things today. First, went back into the LetsDefend Sysmon challenge to go deeper on the specific Event IDs — not just finding findings but understanding what each Event ID actually captures and why it exists. Second, read through SwiftOnSecurity's config and Olaf Hartong's sysmon-modular project on GitHub, then wrote my own custom Sysmon config from scratch.
 
Before today I'd used Sysmon logs to investigate an attack chain. I hadn't really thought about what it takes to configure Sysmon to capture the right things in the first place. That's a completely different skill and it's the one that matters if you're actually deploying detection infrastructure — not just consuming someone else's setup.
 
---

## What Sysmon Actually Is
 
Sysmon is a free Windows system monitoring tool from Microsoft's Sysinternals suite. Once installed it runs as a background service and writes detailed event logs about what's happening on the endpoint — process creation, network connections, file changes, registry modifications, driver loads.
 
Before today I kind of thought of it as a logging tool. After going deeper it's more accurate to think of it as free EDR telemetry. The commercial EDR platforms — CrowdStrike, Carbon Black, MDE — are doing largely the same thing under the hood, just with a nicer interface, automatic alerting, and machine learning on top. Sysmon gives you the raw telemetry. What you do with it is up to you.
 
The catch is that Sysmon out of the box logs almost nothing useful. The default config is minimal. The whole value of Sysmon is in the configuration — what you tell it to log and what you tell it to ignore.
 
---
 
## Event ID Reference
 
Working through the LetsDefend Sysmon logs I focused on finding examples of these five Event IDs:
 
### Event ID 1 — Process Creation
Every time a new process starts, Sysmon logs it. Crucially — it logs the full command line including arguments, the parent process, the user account, and the hash of the executable.
 
**Why it matters:** Most malicious activity involves running something. PowerShell with encoded arguments, cmd.exe spawning from a browser, a script running from the Temp directory — all of these show up in Event ID 1. Without command line logging enabled in Windows, you'd only see that a process ran. Sysmon shows you exactly what it ran.
 
**Example from LetsDefend logs:**
```
EventID: 1
Image: C:\Windows\System32\cmd.exe
CommandLine: cmd.exe /c whoami
ParentImage: C:\Users\Gabr\Downloads\[malicious file]
User: DESKTOP-0V6VB41\Gabr
```
