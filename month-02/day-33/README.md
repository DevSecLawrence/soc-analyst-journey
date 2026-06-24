# Day 33 — EDR Alert Investigation: LetsDefend SOC Analyst Lab

MDE access failed — personal accounts don't qualify for the evaluation lab and the developer sandbox is restricted. Pivoted to LetsDefend's alert monitoring instead. Investigated SOC246 - Forced Authentication Detected: external IP hammering a login endpoint with POST requests, device action permitted, classified as true positive.

The interface changed. The questions didn't.

## Files
- [day33-edr-alert-investigation.md](./day33-edr-alert-investigation.md) — main write-up, what happened, what I concluded
- [day33-alert-investigations/](./day33-alert-investigations/)
  - [SOC246-forced-authentication.md](./day33-alert-investigations/SOC246-forced-authentication.md) — full investigation: forced authentication / credential stuffing alert