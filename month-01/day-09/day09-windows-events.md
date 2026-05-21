# Day 09 — Windows Event Log Deep Dive

Today I focused on the Windows event telemetry that actually tells a story. I enabled command-line logging for process creation, generated a few administrator-level actions on my machine, exported the events, and pulled screenshots so you can see the exact evidence I used.

## Summary (TL;DR)

- I enabled command-line logging for process creation (so `4688` includes the full command line).
- I performed a set of common admin commands locally and captured the resulting events: `4624` (successful logon), `4625` (failed logon), and `4688` (process creation with command line).
- Artifacts (exports and screenshots) are in `event-samples/` and `screenshots/`.

## What I Did

1. Enabled command-line auditing for process creation on my test host.
2. Performed these commands interactively: `ipconfig`, `whoami`, `net user`, `tasklist`, `systeminfo`.
3. Exported the relevant Windows events as XML/EVTX to `event-samples/`.
4. Captured screenshots of the Event Viewer showing the `4688` entries with command line details (see screenshots below).

## Events I Collected

- **Event ID 4624 — Successful Logon**: useful for establishing account context and session start times.
- **Event ID 4625 — Failed Logon**: captures failed authentication attempts and can indicate brute force or mistyped credentials.
- **Event ID 4688 — Process Creation**: with command-line logging enabled, this is gold — it shows the exact command the user ran.

## Key Findings (in my words)

- Enabling command-line logging turned `cmd.exe` from a useless blunt instrument into a readable timeline of intent. With the command line captured, I can tell whether `powershell.exe` was used to run a benign helper or was invoked with a suspicious encoded command.
- `4624` gives me the who/when, `4688` gives me the what. Correlating the two answers the basic triage question: "Who ran what, and when?"
- Failed logons (`4625`) around the same timestamp as odd `4688` calls is a strong indicator of suspicious activity and should escalate to deeper review.

## How I Would Detect This (practical ideas)

- Create a correlation that joins `4625` failures with subsequent `4688` process creations from the same account within a short window (5–10 minutes).
- Alert on `4688` entries where command line contains suspicious patterns: base64 blobs, `-EncodedCommand`, or uncommon execution paths (user profile locations, temp folders).
- Baseline common admin behavior (scheduled tasks, admin tools) to reduce false positives — for example, allow `ipconfig`, `tasklist`, and `systeminfo` but flag scripted or encoded PowerShell usage.

## Artifacts

- Event exports: `event-samples/` (EVTX/XML files for `4624`, `4625`, `4688`).
- Screenshots (process creation with command line):

![Process creation - screenshot 1](./screenshots/Screenshot 2026-05-21 173625.png)

![Process creation - screenshot 2](./screenshots/Screenshot 2026-05-21 173833.png)

![Process creation - screenshot 3](./screenshots/Screenshot 2026-05-21 173935.png)

## Next Steps (what I'll do or recommend)

1. Draft a compact detection rule (Sigma) for `4688` with risky command-line indicators and convert it to Splunk/SIEM format.
2. Tune alerts against normal admin activity captured over a week to reduce noise.
3. Expand playbook: if `4688` + suspicious CLI is detected, collect process memory and perform a file/parent process investigation.

If you want, I can draft the Sigma rule and convert it to a Splunk query next — want me to do that now?

---

Files created/updated during this exercise:

- `month-01/day-09/event-samples/` — exported EVTX/XML examples
- `month-01/day-09/screenshots/` — evidence screenshots

