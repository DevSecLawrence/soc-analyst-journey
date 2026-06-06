# YARA vs Sigma — What's the Difference and When Do You Use Each

This came up naturally doing Day 22. Before today I kind of knew they were different but couldn't explain it properly. After actually writing YARA rules and comparing them to the Sigma rules I wrote on Day 20, it clicked.

---

## The Simple Version

| | Sigma | YARA |
|--|-------|------|
| Scans | Log events | Files and memory |
| Runs in | SIEM (Splunk, Elastic) | Endpoint AV, sandboxes, scanners |
| Detects | Suspicious behaviour (what happened) | Suspicious content (what something contains) |
| Fires when | A log entry matches a pattern | A file matches strings/conditions |
| Written in | YAML | YARA DSL with imports |

---

## How I Think About It Now

**Sigma** = something happened and got logged. A process spawned, a registry key changed, someone logged in from a weird place. Sigma catches behaviour — things you see in event logs after something runs.

**YARA** = something exists on disk or in memory that looks malicious. A file has shellcode in it. A binary has UPX section names. A script has base64-encoded PowerShell. YARA catches presence — things you see when you actually look at the file itself.

---

## They Cover Different Parts of the Kill Chain

```
Malicious file lands on disk
        ↓
YARA scans it → fires on file content  (before execution)
        ↓
File executes
        ↓
Windows event logs generated
        ↓
Sigma rule fires in SIEM → alert       (after execution)
        ↓
Analyst gets both alerts and investigates
```

A file that evades YARA (packed, obfuscated, no known strings) might still get caught by Sigma when it runs and starts doing suspicious things. A file that evades Sigma (runs too quietly, no log entries) might still get caught by YARA sitting on disk. You want both running.

---

## When You'd Use One Over the Other

**Use Sigma when:**
- You're building detections in a SIEM
- You want to alert on specific Windows event IDs
- You're hunting for lateral movement, credential access, or persistence in logs
- You care about the sequence of events, not just the file

**Use YARA when:**
- You're doing malware analysis or sandbox work
- You want to scan endpoints for known-bad files
- You're threat hunting on disk or in memory dumps
- You have a malware sample and want to build a rule to catch variants

---

## Real Example

**Sigma rule:** Alert when `powershell.exe` spawns as a child of `winword.exe` — that's suspicious, Word shouldn't be launching PowerShell.

**YARA rule:** Flag any `.docx` file that contains an embedded OLE object with a macro that references `powershell.exe` — that's the malicious attachment before it even runs.

Both are needed. Sigma catches it when the user opens the document and the macro fires. YARA catches it when the file lands in the email attachment folder before anyone opens it.

---

## Bottom Line

They're not competing tools. They're complementary. A real detection stack runs both. Day 22 was about adding YARA to the toolkit — before today I only had Sigma. Now I have both sides covered.
