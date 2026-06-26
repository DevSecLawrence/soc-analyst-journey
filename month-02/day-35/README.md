# Day 35 — Process Tree Analysis: Understanding Execution Chains

Used Process Hacker on my actual Windows host to baseline normal process trees — what Explorer.exe spawns, what svchost.exe looks like, Chrome's multi-process architecture, what runs at boot. Then documented 5 suspicious process tree patterns from real threat intelligence reports since I'm not running attack simulations on my host machine.

Main thing I learned: you can't spot abnormal until you know normal. The baseline comes first.

## Files
- [day35-process-tree-analysis.md](./day35-process-tree-analysis.md) — main write-up, what I did, what I concluded
- [day35-normal-process-baseline.md](./day35-normal-process-baseline.md) — what normal Windows process trees look like
- [day35-suspicious-patterns.md](./day35-suspicious-patterns.md) — 5 attack patterns with MITRE mappings, sourced from threat reports