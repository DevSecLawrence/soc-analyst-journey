# Day 21 — Sigma Rules

## What I Concluded
Sigma is basically detection logic that travels. The rule stays the same, the SIEM syntax changes. That’s the value. I can write a clean behavioral rule once and then deal with field mapping per platform instead of rewriting the entire detection.

## Assumption I Made
I assumed Sigma conversion would be “push button = perfect query.” It’s not. Field names and log sources don’t line up cleanly across platforms, so conversion is only the starting point.

## Uncertainty I Have
I still don’t have a clean, repeatable way to validate these rules without real logs. I can generate the query, but I need test data to see if it actually fires or if it’s noisy.

## Rules Reviewed (5)
1. Suspicious PowerShell encoded command
2. whoami.exe execution (basic recon)
3. certutil.exe download usage
4. rundll32.exe suspicious execution
5. net.exe user /add behavior

## Rules Written (3)

- whoami.exe execution
- PowerShell encoded command
- New local admin account creation

Notes and rule files live in `./sigma-rules/`.
