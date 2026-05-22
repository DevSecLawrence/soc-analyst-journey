# Day 09 — Windows Event Log Deep Dive: The Logs That Matter

## Medium Exercise — Capturing 4624, 4625, 4688

### What I Did

Opened Event Viewer → Windows Logs → Security → filtered 
for Event IDs 4624, 4625, and 4688 all at once. Got 834 
events back across the three IDs. That number alone tells 
you something — Windows is logging constantly in the 
background without you doing anything.

---

### Event ID 4624 — Successful Logon

Every entry I saw was **Logon Type 5** — service logon. 
That means Windows itself was logging in to start services, 
not a human sitting at the keyboard. The account was SYSTEM 
and the process was services.exe.

Breaking down the key fields:

- **Security ID:** SYSTEM
- **Account Name:** LAWRENCES
- **Logon Type:** 5 (Service)
- **Process Name:** C:\Windows\System32\services.exe
- **Source IP:** - (local, no network source)

Logon Type is the most important field here. The types 
that matter most in a SOC context:

| Type | Name | When you'd see it |
|---|---|---|
| 2 | Interactive | Someone physically sitting at the machine |
| 3 | Network | Remote access, mapped drives, lateral movement |
| 5 | Service | Windows starting a service — usually noise |
| 10 | RemoteInteractive | RDP login — high value for detection |

Type 5 is almost always noise. Type 3 and Type 10 are 
what you'd flag for investigation.

---

### Event ID 4625 — Failed Logon

This is the detection gold standard for brute force. 
A single 4625 is nothing. But 50 of them from the same 
source IP in 60 seconds is a brute force attempt.

The fields that matter:
- **TargetUserName** — what account was targeted
- **LogonType** — how they were trying to log in
- **IpAddress** — where it came from
- **FailureReason** — wrong password vs unknown username

Unknown username failures are more interesting than wrong 
passwords — it means the attacker is guessing account names, 
not just passwords.

---

### Event ID 4688 — Process Creation

This is where command-line logging matters. The events 
from 16/05/2026 showed process creation but the CommandLine 
field was blank — because the registry key wasn't set yet.

Without command-line logging:
New Process: cmd.exe
Command Line: (blank)


That tells me cmd.exe ran. Nothing else. Useless for 
detection.

---

## Hard Exercise — Enabling Command-Line Logging

### What I Changed

**Registry:**

Path:
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion
Policies\System\Audit


Created new DWORD value:
ProcessCreationIncludeCmdLine_Enabled = 1


**Group Policy:**

Navigated to:
Computer Configuration → Windows Settings → Security Settings →
Advanced Audit Policy Configuration → System Audit Policies →
Detailed Tracking → Audit Process Creation


Set to: **Success**

Then ran:
```cmd
gpupdate /force
```

Both changes confirmed from my screenshots — the registry 
shows `0x00000001 (1)` and Group Policy shows 
`Audit Process Creation = Success`.
 
Registry and Group Policy confirmations (screenshots):

![Registry ProcessCreationIncludeCmdLine_Enabled](./screenshots/Screenshot%202026-05-21%20173625.png)
Registry: `ProcessCreationIncludeCmdLine_Enabled = 1` (confirmed in Registry Editor)

![Group Policy Audit Process Creation](./screenshots/Screenshot%202026-05-21%20173833.png)
Group Policy: `Audit Process Creation = Success` (Advanced Audit Policy view)

---
---

### Running the 5 Recon Commands

After enabling command-line logging I opened Command Prompt 
and ran these one by one:

```cmd
ipconfig
whoami
net user
tasklist
systeminfo
```

Each one generated a 4688 event. With command-line logging 
now enabled, the events looked completely different:

**Before (no cmd-line logging):**
New Process Name: C:\Windows\System32\ipconfig.exe
Command Line:     (blank)


**After (cmd-line logging enabled):**
New Process Name:    C:\Windows\System32\ipconfig.exe
Command Line:        ipconfig
Parent Process Name: C:\Windows\System32\cmd.exe
Subject User Name:   USER


The difference is everything. Now I can see what actually 
ran, not just that something ran.

Before/After event screenshots:

![Before - CommandLine Blank](./screenshots/Screenshot%202026-05-21%20173935.png)
Caption: 4688 events BEFORE enabling command-line logging — CommandLine field empty.

![After - CommandLine Present](./screenshots/Screenshot%202026-05-22%20200950.png)
Caption: 4688 events AFTER enabling command-line logging — CommandLine populated with executed command.
---

### What Each Command Reveals to a Defender

| Command | What it does | Why an attacker runs it |
|---|---|---|
| ipconfig | Shows all network interfaces and IPs | Map the network, find gateways |
| whoami | Shows current user and privileges | Check if they have admin rights |
| net user | Lists all local user accounts | Find accounts to target or pivot to |
| tasklist | Lists all running processes | Check for AV/EDR before dropping malware |
| systeminfo | Full OS info, hotfixes, domain info | Identify patch gaps to exploit |

Individually any of these could be a legitimate admin 
checking something. Together in sequence within a short 
time window — that's reconnaissance.

---

### Detection Concept — What Makes This Recon vs Legitimate Admin

This is the hard question. The commands themselves aren't 
malicious. `whoami` is built into Windows. `ipconfig` is 
what you run when the internet stops working. The detection 
isn't in any single event — it's in the pattern.

**Signal 1 — Sequence**

A legitimate admin runs `ipconfig` to diagnose a network 
issue. An attacker runs `ipconfig`, then `whoami`, then 
`net user`, then `tasklist`, then `systeminfo` — all within 
30 seconds. That sequence is a checklist. Nobody diagnoses 
a network issue by checking their own username first.

**Signal 2 — Parent Process**

Legitimate tools launched by a human come from explorer.exe 
or a known application. Suspicious process chains look like:
cmd.exe spawned by powershell.exe
spawned by winword.exe


Word spawning PowerShell spawning cmd is not normal admin 
behavior. That's a macro executing a shell.

**Signal 3 — User Context**

`whoami` run by a domain admin during business hours from 
their workstation = probably fine. `whoami` run by 
SYSTEM or a service account outside business hours = 
worth investigating.

**Signal 4 — Command Frequency**

5 recon commands in 30 seconds from one process = automated 
tooling. Humans don't type that fast. Automated recon 
scripts do.

**The baseline problem:**

The reason none of this is simple is that these commands 
are run by legitimate admins all the time. The only way 
to build a reliable detection is to know your baseline — 
what's normal for your specific environment. That's why 
the brutal mentor note says "if your org doesn't have 
command-line logging, you're blind." You can't build a 
baseline without the data in the first place.

---

## What I Concluded

The biggest thing today wasn't the event IDs themselves — 
it was realising that process creation logging without 
command-line arguments is basically useless for detection. 
You see that cmd.exe ran. You don't see what it ran. That's 
like a security camera that only records that a person 
entered a room but not what they did inside.

Enabling `ProcessCreationIncludeCmdLine_Enabled` is a 
one-line registry change that dramatically improves 
endpoint visibility. The fact that it's not on by default 
in Windows is a serious gap that most organisations don't 
know about until they're already in an incident and the 
logs are empty.

The three event IDs together tell a story. 4624 tells you 
who was on the machine. 4688 tells you what they ran. 4625 
tells you who tried and failed. Without all three you have 
an incomplete picture.

## Assumption I Made

I assumed process creation logging was enabled by default. 
It wasn't. The 4688 events from before I made the registry 
change all had blank CommandLine fields — I could see 
processes were created but had no idea what commands were 
actually run. That assumption would be dangerous in a real 
SOC environment — you'd run a search for command-line 
indicators and get zero results, assume nothing happened, 
and miss the whole attack.

## Uncertainty I Have

I still don't fully understand how to distinguish attacker 
recon from legitimate admin activity at scale. The pattern 
logic I documented above makes sense for manual analysis. 
But how does a SIEM rule encode "5 recon commands in 30 
seconds from the same process"? That requires correlation 
logic across multiple events, not just a single field match.

I want to build that detection rule properly when I get 
to Month 2 SIEM work. For now I understand the concept — 
context, sequence, and frequency matter more than any 
single command