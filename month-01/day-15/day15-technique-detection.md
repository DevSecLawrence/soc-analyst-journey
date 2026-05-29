# Day 15 — Technique Detection (1 Technique, written like a real rule)

## Technique Chosen

- Technique ID + name: T1574.002 — Hijack Execution Flow: DLL Side-Loading
- Why I chose it (relevance / common / realistic): This is one of those techniques that SOCs actually run into. It’s also perfect for “looks normal at a glance” attacks.
- Threat report it came from: DEV-0139 launches targeted attacks against the cryptocurrency industry (Microsoft Threat Intelligence)

---

## What I’m Trying to Detect (Plain English)

“A legit-looking EXE is running from a weird folder, with weird arguments, and it’s probably being used to load a malicious DLL next to it.”

In the DEV-0139 chain specifically, the report describes:
- `logagent.exe` running from a weird location and side-loading a malicious `wsock32.dll`
- `TPLink.exe` side-loading a malicious `DUser.dll`
- command lines that include a GUID-like value plus an XOR key argument (examples include `/shadow` and `/sven`)

---

## Telemetry Needed

For this technique, I need:
- Host evidence:
	- suspicious process execution (unusual path + unusual args)
	- bonus points if I can see module/DLL loads (that’s the “confirm sideload” part)
- Fields that should exist if logging is good:
	- `process.name`, `process.executable`, `process.command_line`
	- `host.name`, `user.name`
	- (Nice to have) parent process fields
	- (Best) module/DLL load fields from Sysmon or EDR

---

## Log Sources That Provide It

Pick what you actually have access to:
- Sysmon (best for a home lab)
	- Event ID 1: Process Create
	- Event ID 7: Image/DLL loaded (high value for sideload)
- EDR telemetry (if you have Elastic Defend, even better)
- Windows Security logs (only helps if you have process creation auditing configured, and even then it can be limited)

---

## Detection Logic

### Option A — Elastic (KQL / Rule)

**KQL filter**
```
event.category:process and
process.name:("logagent.exe" or "TPLink.exe") and
(
	process.command_line:("* /shadow*" or "* /sven*") or
	process.executable:("C:\\ProgramData\\SoftwareCache\\logagent.exe" or "C:\\Users\\*\\AppData\\Roaming\\Dashboard_v2\\TPLink.exe")
)
```

Why this query (in plain terms):
- I’m not trying to detect “all DLL sideloading on Earth.”
- I’m trying to detect *this report’s pattern* first (high signal), then broaden later.

**Rule type**
- Query rule (Custom query)

**Threshold design**
- Group by: `host.name`, `process.executable`, `user.name`
- Window: 15m
- Threshold: 1 (this is already high-signal if you keep the query specific)

### Option B — Splunk (SPL)

Not built today — I focused on Elastic for this lab.

---

## Tuning / False Positives

- What normal behavior could look like this?
	- Someone renames stuff in a lab (or a messy IT environment).
	- Weird internal software packaging scripts.
- What allowlists make sense?
	- Known lab hosts (mine)
	- Known software deployment accounts
- What extra context would make this way stronger?
	- Parent process logic (Excel → weird EXE in ProgramData is a big red flag)
	- DLL load visibility (Sysmon EID 7 / EDR module load) to confirm the sideload path

---

## How I Would Test It

- How would I generate a safe signal in a lab?
	- Copy any benign EXE (like `notepad.exe`) into a folder you control.
	- Rename it to `logagent.exe`.
	- Run it with the argument: `/shadow`.
	- That gives me a clean “process event” I can search for without doing anything actually malicious.
- What result would prove it’s working?
	- In Elastic Discover: I can find the event with the exact KQL.
	- In Elastic Security (once I build the rule): I get an alert and can open the alert details.

---

## What’s Missing (Proof)

This doc is the detection *plan*.

To make it legit proof for Day 15, I still need screenshots of:
1) the Elastic rule showing the KQL
2) the rule enabled
3) at least one alert firing (or at minimum, the matching event in Discover)
