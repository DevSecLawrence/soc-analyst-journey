# Day 36 — PowerShell Logging Configuration Guide

**Date:** 2026-06-27
**Tested on:** Windows 11 (personal host)

A step-by-step reference for enabling all three PowerShell logging mechanisms. Written from what I actually did today, not from documentation.

---

## Why You Need This

Without PowerShell logging, Windows tells you `powershell.exe` ran. That's it. With logging enabled, you know what commands ran, what modules were used, and have a full transcript of the session. For a SOC analyst — or anyone trying to detect attackers using PowerShell — this is non-negotiable.

---

## Step 1 — Open Group Policy Editor

Press `Win+R` → type `gpedit.msc` → Enter

Navigate to:
```
Computer Configuration
  └── Administrative Templates
        └── Windows Components
              └── Windows PowerShell
```

You'll see 5 settings. We're enabling 3 of them.

---

## Step 2 — Enable Script Block Logging (Event ID 4104)

1. Double-click **Turn on PowerShell Script Block Logging**
2. Select **Enabled**
3. Click **OK**

**What this captures:** The actual code that executes — including deobfuscated content. Even if a command was base64-encoded, you see the decoded version.

**Where to verify:**
```
Event Viewer → Applications and Services Logs → Microsoft → Windows → PowerShell → Operational
Filter by: Event ID 4104
```

Run any PowerShell command and Event ID 4104 entries will appear immediately.

---

## Step 3 — Enable Module Logging (Event ID 4103)

1. Double-click **Turn on Module Logging**
2. Select **Enabled**
3. In the Options section, click **Show** next to Module Names
4. In the Value column, type `*` (asterisk logs all modules)
5. Click **OK** → **OK**

**What this captures:** Every PowerShell module loaded and every function called, with input parameters and output.

**Where to verify:**
```
Event Viewer → same location
Filter by: Event ID 4103
```

---

## Step 4 — Enable Transcription

1. Double-click **Turn on PowerShell Transcription**
2. Select **Enabled**
3. In the Options section, set a **Transcript output directory** — e.g. `C:\PSTranscripts`
4. Optionally check **Include invocation headers** for timestamps on every command
5. Click **OK**

**What this captures:** A complete text file of everything typed and every output in a PowerShell session. Saved as a `.txt` file in the directory you specified.

**Where to verify:**
Open a new PowerShell window, run a few commands, close it. Navigate to `C:\PSTranscripts` — you'll find a text file with the full session recorded.

**Note:** Create the `C:\PSTranscripts` folder first if it doesn't exist, or choose a directory that already exists.

---

## Step 5 — Verify All Three Are Active

After enabling, your Group Policy Windows PowerShell section should show:

| Setting | State |
|---------|-------|
| Turn on Module Logging | Enabled |
| Turn on PowerShell Script Block Logging | Enabled |
| Turn on PowerShell Transcription | Enabled |

---

## Quick Test

Open PowerShell and run:
```powershell
Get-Process
whoami
$env:USERNAME
```

Then check:
1. Event Viewer for Event ID 4103 and 4104 entries
2. Your transcript directory for a new `.txt` file

All three should show activity from these commands.

---

## Important Note

Enabling these on a production machine generates significant log volume. On my personal machine, 2,001 events appeared in the PowerShell Operational log just from background system activity — no manual commands at all. In an enterprise environment with hundreds of endpoints this would be enormous. Make sure your log retention and SIEM ingestion capacity can handle the volume before enabling in production.
