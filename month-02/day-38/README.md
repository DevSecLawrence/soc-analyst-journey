# Day 38 — Windows Persistence Mechanisms

I mapped the main Windows persistence locations and wrote detections for the ones attackers use most. The local Windows VM was down, so I leaned on ATT&CK, vendor docs, and browser-lab telemetry to keep the work moving.

## Files
- [day38-persistence.md](./day38-persistence.md) — main write-up
- [day38-persistence-baseline.md](./day38-persistence-baseline.md) — normal persistence locations and what to watch
- [day38-persistence-detections/](./day38-persistence-detections/) — 5 Sigma rules