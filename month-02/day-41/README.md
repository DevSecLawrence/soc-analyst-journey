# Day 41 — Data Exfiltration Patterns

The final stage — data leaving the network. If you're detecting here, earlier defences already failed. But catching it here is still better than not catching it at all.

Researched 5 exfiltration techniques: HTTP/HTTPS uploads, DNS tunneling, cloud storage abuse, email exfiltration, and protocol tunneling (ICMP). The common thread across all of them: legitimate channels, anomalous behaviour. You can't block HTTPS or DNS — you have to detect the pattern.

5 Sigma detection rules written, one per technique. All research-based — lab still down.

## Files
- [day41-exfiltration.md](./day41-exfiltration.md) — how each technique works, detection opportunities, conclusions
- [day41-exfil-techniques.md](./day41-exfil-techniques.md) — quick reference table, detection priority order, baseline problem
- [day41-exfil-detections/](./exfil-detections/) — 5 Sigma detection rules
- [screenshots](./screenshots/)- Screenshots