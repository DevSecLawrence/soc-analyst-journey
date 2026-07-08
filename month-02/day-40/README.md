# Day 40 — Lateral Movement Detection

Attackers don't stop at the first machine they compromise. Today was about understanding how they move — PSExec, WMI, WinRM, RDP, remote scheduled tasks — and how defenders detect the movement. Windows VM still down so this is research and detection writing, not hands-on simulation. 5 Sigma rules written, one per technique.

The hardest part isn't detecting the tools — it's distinguishing attacker use from legitimate admin use. Same tools, different context.

## Files
- [day40-lateral-movement.md](./day40-lateral-movement.md) — how each technique works, artifacts, detection opportunities, conclusions
- [day40-lateral-techniques.md](./day40-lateral-techniques.md) — quick reference table, logon types guide, admin vs attacker patterns
- [day40-lateral-detections/](./day40-lateral-detections/) — 5 Sigma detection rules
- [screenshots](./screenshots/)