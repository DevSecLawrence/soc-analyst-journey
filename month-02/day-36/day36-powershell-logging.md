# Day 36 — PowerShell Logging and Analysis

**Date:** 2026-06-27
**Machine:** Windows host (personal machine)
**Tools:** Group Policy Editor (gpedit.msc), Event Viewer, PowerShell 5.1

---

## What I Did

Enabled all three PowerShell logging mechanisms on my Windows host using Group Policy, ran commands to verify each one was actually capturing data, then analysed 5 malicious PowerShell patterns from real threat reports and wrote Sigma detection rules for each.

Before today I knew PowerShell was commonly abused by attackers. What I didn't fully appreciate was how blind you are to it without logging enabled. Without these settings turned on, Windows only tells you that powershell.exe ran. With them on, you can see exactly what it ran, what modules it used, and every command typed in the session.

---

## The Three Logging Mechanisms

### 1. Script Block Logging — Event ID 4104

**What it does:** Logs the actual code that executes — including deobfuscated content. If an attacker uses base64 encoding to hide a malicious command, Script Block Logging captures the decoded version after PowerShell processes it.

**How I enabled it:**
- Win+R → `gpedit.msc`
- Computer Configuration → Administrative Templates → Windows Components → Windows PowerShell
- Double-clicked **Turn on PowerShell Script Block Logging** → Enabled → OK

**Verified it works:**
Opened PowerShell → ran `Get-Process` → went to Event Viewer → Applications and Services Logs → Microsoft → Windows → PowerShell → Operational → saw Event ID 4104 entries immediately.

The event showed:
```
Creating Scriptblock text (1 of 1):
prompt

ScriptBlock ID: 65a60ea8-07a7-40ed-96ba-7539f25bf90b
```

Even just opening PowerShell generated logs — it captured the `prompt` function that draws the `PS C:\>` display. 2,001 events were already in the log from normal system activity. That's how much PowerShell runs in the background on a normal Windows machine without you even touching it.

**Why it matters for detection:** This is the one that catches obfuscated attacks. An attacker runs `-EncodedCommand` with base64. Windows decodes it to execute it. Script Block Logging captures it after decoding — so you see the real command, not the encoded version.

---

### 2. Module Logging — Event ID 4103

**What it does:** Logs every PowerShell module that gets loaded and every function called from those modules — including the input parameters and output.

**How I enabled it:**
- Same Group Policy location
- Double-clicked **Turn on Module Logging** → Enabled → in Options clicked Show → typed `*` to log all modules → OK

**Verified it works:**
Ran `Get-Process` again → checked Event Viewer for Event ID 4103 entries → confirmed they appeared.

**Why it matters for detection:** Script Block Logging shows you what code ran. Module Logging shows you what capabilities were invoked. If an attacker uses `Invoke-Mimikatz` or any known offensive PowerShell module, Event ID 4103 will log the function call and its parameters even if the code was obfuscated.

---

### 3. Transcription

**What it does:** Writes a complete text file of everything typed in a PowerShell session — every command, every output. Like a screen recording but in text form.

**How I enabled it:**
- Same Group Policy location
- Double-clicked **Turn on PowerShell Transcription** → Enabled → set output directory → OK
- Group Policy showed "Yes" in the Comment column confirming the output directory was set

**Why it matters for detection:** Transcription is the most human-readable log. Event ID 4103 and 4104 entries are structured but require Event Viewer to read. A transcription file is a plain text document you can open in Notepad and read like a conversation log. For forensics — reconstructing what an attacker did during an intrusion — transcription files are extremely useful.

---

## Final Group Policy State

After enabling all three, Group Policy showed:

| Setting | State |
|---------|-------|
| Turn on Module Logging | Enabled |
| Turn on PowerShell Script Block Logging | Enabled |
| Turn on PowerShell Transcription | Enabled (Yes — output directory set) |
| Turn on Script Execution | Not configured |

All three logging mechanisms active simultaneously on my Windows host.

---

## What I Concluded

PowerShell logging is one of those things where you don't realise how blind you were until you turn it on. Before enabling these I had no idea that just opening a PowerShell window was generating logs of what the prompt function was doing. After enabling them — 2,001 events in the log from background system activity alone, and that's on a personal machine, not an enterprise endpoint.

The thing that really clicked: Script Block Logging defeats obfuscation. An attacker encoding their command in base64 is trying to hide what they're running from simple string inspection. Script Block Logging captures the command after Windows decodes it to execute it. You always see the real thing.

Without logging enabled, an attacker can run PowerShell all day and leave almost no trace. With it enabled, every command they run is recorded. This is not optional visibility — it's foundational.

---

## Assumption I Made

I assumed encoded PowerShell commands were always malicious. They're not — some legitimate software and admin tools use base64 encoding in their PowerShell commands, usually to handle special characters or to pass complex parameters without quoting issues. The encoding itself isn't the indicator. The combination of encoding plus suspicious content (download cradles, AMSI bypass attempts, credential access) is what makes something malicious. Script Block Logging lets you see the decoded content so you can make that judgement.

---

## Uncertainty I Have

I don't know how to detect PowerShell that downloads and executes entirely in memory without ever writing to disk. Script Block Logging captures what runs in the PowerShell session, but if a payload is downloaded via `IEX (New-Object Net.WebClient).DownloadString()` and runs entirely in memory, I'm not sure how much of it ends up in Event ID 4104. I think Script Block Logging does capture in-memory execution — but I haven't verified this with a real example and I want to before I'm confident about it.
