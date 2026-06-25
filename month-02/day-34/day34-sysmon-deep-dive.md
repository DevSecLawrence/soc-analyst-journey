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
### Event ID 3 — Network Connection
Every outbound network connection an application makes. Logs the source process, source IP/port, destination IP/port, and whether it was initiated or received.
 
**Why it matters:** Malware almost always needs to communicate — downloading a payload, sending stolen data, receiving commands from C2. Event ID 3 shows you what process made the connection, not just that a connection was made. A network firewall log shows you the traffic. Sysmon Event ID 3 shows you which process on which machine generated it.
 
**Example from LetsDefend logs:**
```
EventID: 3
Image: C:\Windows\System32\powershell.exe
DestinationIp: [edit with actual IP from challenge]
DestinationPort: 4422
Initiated: true
```
 
### Event ID 7 — Image Loaded
Every time a process loads a DLL or module. Logs the process that loaded it, the path of the DLL, and the hash.
 
**Why it matters:** DLL injection and DLL hijacking both involve loading malicious code into a legitimate process. If malware injects into explorer.exe by loading a malicious DLL, Event ID 7 shows explorer.exe loading a DLL from an unusual path — a path that doesn't match where that DLL should live.
 
This one generates a lot of noise because legitimate software loads hundreds of DLLs. Good Sysmon configs filter out known-good DLLs aggressively and only alert on ones loading from unusual locations.
 
### Event ID 11 — File Created
Every time a file is written to disk. Logs the process that created it and the target path.
 
**Why it matters:** Malware dropping files — payloads, scripts, persistence files — all show up here. The most suspicious patterns are files being created in Temp directories, AppData, or other non-standard locations by processes that have no business writing files there. A browser dropping a .exe into Temp is not normal.
 
### Event ID 13 — Registry Value Set
Every time a registry value is written. Logs which process wrote it, which key and value was modified, and what the new data is.
 
**Why it matters:** Registry run keys are one of the most common persistence mechanisms. `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` being written by anything other than a known installer should always be investigated. Event ID 13 catches this at the moment it happens, not after the machine reboots and the malware is already running.
 
---

## What I Concluded
 
The gap between "Sysmon installed" and "Sysmon useful" is entirely configuration. SwiftOnSecurity's config is nearly 1,500 lines long. Every line is a decision about what to log and what to exclude. Too permissive and you're generating gigabytes of noise that drowns out real signals. Too restrictive and you're missing the attacks you care about.
 
Reading through Olaf Hartong's sysmon-modular project showed me that serious detection engineers treat Sysmon config like code — versioned, tested, modular, with specific rules for specific threat scenarios. That's a completely different mindset from "install and forget."
 
The other thing that clicked: Sysmon is the answer to the MDE access problem from Day 33. Can't afford CrowdStrike? Can't get MDE access? Sysmon gives you endpoint telemetry that's good enough to catch most of what commercial EDR catches, for free, if you configure it properly. That's a genuinely useful skill for smaller organisations that can't spend $20 per endpoint per month on commercial EDR.
 
---
 
## Assumption I Made
 
I assumed the default Sysmon install was doing something useful. After reading SwiftOnSecurity's config I realised the default logs almost nothing. The config is the entire value. Installing Sysmon without a proper config is like buying a CCTV system and pointing all the cameras at the ceiling — technically installed, functionally useless.
 
---
 
## Uncertainty I Have
 
I wrote a custom config today but I haven't tested it. I don't know if my filtering logic is correct — specifically whether my exclusion rules are too broad (accidentally excluding malicious activity that looks like known-good noise) or too narrow (still logging too much noise). The only way to know is to deploy it in a real lab, generate known attack activity, and verify that the config catches what it should and ignores what it should. That testing has to wait until the Windows VM is rebuilt.
