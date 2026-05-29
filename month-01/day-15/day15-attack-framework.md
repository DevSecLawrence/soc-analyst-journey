# Day 15 — MITRE ATT&CK: Threat Report → Technique IDs → “So what do I detect?”

## What I Concluded

Today was me using ATT&CK the way it’s actually supposed to be used (in my opinion):

- not memorizing the matrix
- not collecting technique IDs like Pokémon
- actually translating a real report into a set of behaviors I can talk about + eventually detect

Not gonna lie: the hard part isn’t finding an ID. The hard part is being honest and specific.

Like… do I really have enough evidence from the report to call it a sub-technique? Or am I forcing it?

Also: a technique ID is not a detection.

A detection is:
technique + telemetry + environment context + tuning.

---

## The Two Threat Reports I Used

Report #1
- Title: DEV-0139 launches targeted attacks against the cryptocurrency industry
- Link: https://www.microsoft.com/en-us/security/blog/2022/12/06/dev-0139-launches-targeted-attacks-against-the-cryptocurrency-industry/
- Who published it (Microsoft / Mandiant / CrowdStrike / etc): Microsoft Threat Intelligence

Report #2
- Title: New XCSSET malware adds new obfuscation, persistence techniques to infect Xcode projects
- Link: https://www.microsoft.com/en-us/security/blog/2025/03/11/new-xcsset-malware-adds-new-obfuscation-persistence-techniques-to-infect-xcode-projects/
- Who published it: Microsoft Threat Intelligence

Quick note:
- Report #1 is basically “Windows lure → macro → loader → DLL sideload → C2”.
- Report #2 is “macOS developer supply chain-ish infection (Xcode projects) + scripting + persistence + stealing stuff + exfil”.

---

## Techniques I Extracted (Evidence-Based)

### Report #1 Techniques

| Tactic | Technique ID | Technique Name | Why I mapped it (the exact behavior/quote I saw) |
|---|---|---|---|
| Reconnaissance | T1591 | Gather Victim Org Information | They didn’t just spam people — they came in with real industry context to build trust. |
| Reconnaissance | T1593.001 | Search Open Websites/Domains: Social Media | They found targets through Telegram groups and reached out there. |
| Resource Development | T1583.001 | Acquire Infrastructure: Domains | They registered/used a C2 domain (strainservice[.]com). |
| Initial Access | T1566.001 | Phishing: Spearphishing Attachment | The lure is a weaponized Excel attachment. |
| Execution | T1204.002 | User Execution: Malicious File | User has to open it + enable macros. |
| Execution | T1059.005 | Command and Scripting Interpreter: Visual Basic | VBA/macros do the staging + execution. |
| Execution | T1106 | Native API | Report calls out CreateProcess usage. |
| Defense Evasion | T1574.002 | Hijack Execution Flow: DLL Side-Loading | Legit EXEs are used to load malicious DLLs (classic sideload + proxying). |
| Defense Evasion | T1027 | Obfuscated Files or Information | UserForm abuse to hide data/variables. |
| Defense Evasion | T1036.005 | Masquerading: Match Legitimate Name or Location | Looks legit on purpose (DLL names like wsock32.dll + “normal” paths). |
| Defense Evasion | T1027.009 | Obfuscated Files or Information: Embedded Payloads | Payload is staged/embedded and then loaded/decrypted instead of being obvious. |
| Command and Control | T1071.001 | Application Layer Protocol: Web Protocols | C2 over web protocols/ports. |
| Command and Control | T1132 | Data Encoding | Encodes data with the C2. |
| Exfiltration | T1041 | Exfiltration Over C2 Channel | Has the ability to exfil back over C2. |

### Report #2 Techniques

| Tactic | Technique ID | Technique Name | Why I mapped it (the exact behavior/quote I saw) |
|---|---|---|---|
| Initial Access | T1195.001 | Supply Chain Compromise: Compromise Software Dependencies and Development Tools | It infects Xcode projects so the payload runs during builds and spreads through shared project files. |
| Execution | T1059.004 | Command and Scripting Interpreter: Unix Shell | Lots of shell scripting + “pipe it to shell” behavior. |
| Execution | T1059.002 | Command and Scripting Interpreter: AppleScript | Uses AppleScript + compiled AppleScript apps to run stages. |
| Execution | T1059.007 | Command and Scripting Interpreter: JavaScript | Uses JavaScript payloads to pull data (like Notes contents). |
| Defense Evasion | T1140 | Deobfuscate/Decode Files or Information | The whole chain is “decode → decode → decode → execute” (xxd + Base64). |
| Defense Evasion | T1027.013 | Obfuscated Files or Information: Encrypted/Encoded File | Encoded blobs/modules instead of clean scripts. |
| Defense Evasion | T1027.004 | Obfuscated Files or Information: Compile After Delivery | Compiles “run-only” apps to make reversing harder. |
| Command and Control | T1105 | Ingress Tool Transfer | Pulls more tools/modules from C2. |
| Discovery | T1082 | System Information Discovery | Collects system info (OS, SIP/firewall status, etc.). |
| Discovery | T1518 | Software Discovery | Checks for apps like Xcode/Git and changes behavior based on that. |
| Discovery | T1518.001 | Software Discovery: Security Software Discovery | Checks XProtect/MRT versions. |
| Discovery | T1614.001 | System Location Discovery: System Language Discovery | Pulls locale/language. |
| Discovery | T1033 | System Owner/User Discovery | Checks username / owner context. |
| Discovery | T1217 | Browser Information Discovery | Enumerates browser extensions / metadata. |
| Discovery | T1083 | File and Directory Discovery | Searches for Xcode projects, zips, files. |
| Collection | T1005 | Data from Local System | Steals local data. |
| Collection | T1560 | Archive Collected Data | Archives what it stole. |
| Exfiltration | T1041 | Exfiltration Over C2 Channel | Sends it back over C2. |
| Persistence | T1546.004 | Event Triggered Execution: Unix Shell Configuration Modification | Persists via shell config modification (zsh-related persistence). |
| Persistence | T1647 | Plist File Modification | Uses plist modifications for stealth/persistence behaviors. |
| Defense Evasion | T1548.006 | Abuse Elevation Control Mechanism: TCC Manipulation | Tries to reset/abuse TCC controls when blocked. |
| Defense Evasion | T1070.004 | Indicator Removal: File Deletion | Cleans up artifacts. |
| Defense Evasion | T1564.001 | Hide Artifacts: Hidden Files and Directories | Uses hidden files/dirs. |
| Defense Evasion | T1564.003 | Hide Artifacts: Hidden Window | Hides UI/background style execution. |
| Defense Evasion | T1036.005 | Masquerading: Match Legitimate Name or Location | Fake apps that look real (Launchpad/Reminders style). |
| Defense Evasion | T1222.002 | File and Directory Permissions Modification: Linux and Mac File and Directory Permissions Modification | Permission changes show up as part of staging/persistence flows. |

---

## Navigator Layers (What I Built)

- Saved exports:
  - `day15-navigator-layers/report-1-layer.json`
  - `day15-navigator-layers/report-2-layer.json`

(Optional) Screenshot proof:
- `screenshots/navigator-report-1.png`
- `screenshots/navigator-report-2.png`

What this proves (once I screenshot it):
- I can take a report and represent it visually on the matrix.
- I can separate “report 1 behavior” vs “report 2 behavior.”

---

## Assumption I Made

- I assumed “having a technique ID” means I did the work. Nope. That’s just labeling.
- For the XCSSET report, I’m also being real: the article lists techniques, but I’m *inferring tactics* in my own table. That’s my best judgment, not a guarantee.

---

## Uncertainty I Have

- How do I choose what’s worth an actual alert rule vs what’s better as a hunting query?
- When do “generic techniques” (encoding/obfuscation) become too broad unless I add context?
- In Navigator: should I start scoring techniques (confidence/impact) instead of just highlighting everything?

---

## What’s Missing (Proof I Still Need)

Right now this doc proves my mapping + thinking.

It does NOT prove I actually imported the layers yet.

To make Day 15 “real”, I still need to:
1) import both JSON layers into ATT&CK Navigator
2) screenshot each layer view
3) tie one technique to a real detection rule in my SIEM (I wrote that in the detection doc)
