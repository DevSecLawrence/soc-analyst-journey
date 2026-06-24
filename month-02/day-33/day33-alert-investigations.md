# Day 33 — EDR Alert Investigation: LetsDefend SOC Analyst Lab
 
**Date:** 2026-06-24
**Platform:** LetsDefend — Monitoring → Alert Queue
**Original plan:** Microsoft Defender for Endpoint Evaluation Lab
 
---
 
## What Actually Happened
 
The plan was to use the MDE Evaluation Lab. Didn't work out. MDE requires an organisational Microsoft account — personal Gmail gets an AADSTS500200 error blocked at sign-in. Tried the Microsoft 365 Developer Program as a workaround and got "You don't currently qualify for a sandbox subscription." Microsoft has been tightening access to the dev sandbox recently and my account didn't meet whatever criteria they check for.
 
Rather than spending the whole day fighting access issues I pivoted to LetsDefend's alert monitoring feature. The investigation workflow is the same — real alerts, real triage decisions, same questions. The interface is different but the methodology isn't.
 
---
 
## The Alert Queue
 
Opened LetsDefend → Monitoring → Alert. Saw the following active alerts:
 
| Severity | Date | Alert | Category |
|----------|------|-------|----------|
| Medium | Mar 07, 2024 | SOC176 - RDP Brute Force Detected | Brute Force |
| Medium | Feb 28, 2024 | SOC205 - Malicious Macro has been executed | Malware |
| Medium | Dec 27, 2023 | SOC250 - APT35 HyperScrape Data Exfiltration Tool Detected | Data Leakage |
| Medium | Dec 12, 2023 | SOC246 - Forced Authentication Detected | Web Attack |
 
First thing I noticed: all four alerts are Medium severity. In a real SOC queue you'd expect a mix — the fact that everything here is Medium tells me this is a curated learning environment, not a real noisy SOC feed where you'd have hundreds of Low and Informational alerts alongside the meaningful ones.
 
I chose SOC246 - Forced Authentication Detected to investigate first because "Web Attack" was the category I'd spent the least time with so far, and forced authentication is a technique I hadn't seen before.
 
---

