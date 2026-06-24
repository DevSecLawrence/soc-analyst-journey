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

## What I Concluded
 
The biggest thing today wasn't the investigation itself — it was the access issue with MDE. That's a real-world problem. Tools that look freely accessible turn out to require enterprise infrastructure, organisational accounts, or paid licenses that aren't realistic for a student in Nigeria to get through the normal route.
 
What I learned from that: in a real SOC job, the tool is provided. You just need to understand the investigation methodology well enough to apply it in whatever tool the organisation uses. LetsDefend uses a different interface than MDE but the questions I asked — what triggered this, where did it come from, what was the target, what action was taken, is this a true positive — are exactly the same questions I'd ask in MDE, Splunk, or any other platform.
 
The interface is a tool. The methodology is the skill.
 
---
 
## Assumption I Made
 
I assumed the MDE Developer Program sandbox would work for anyone. It doesn't — Microsoft added restrictions at some point and accounts without an active development footprint get blocked. I wasted about 30 minutes on this before pivoting. Next time I hit an access wall I'll give it one serious attempt and move on faster rather than trying the same approach multiple ways.
 
---
 
## Uncertainty I Have
 
I still haven't done hands-on work in an actual EDR console with real telemetry — process trees, memory events, file system monitoring. LetsDefend gives me alert triage experience but the deep endpoint forensics side of EDR is something I haven't touched yet. I need to find a way to get real EDR hands-on time. Either through a university resource, a CTF that uses EDR telemetry, or eventually through a job. This is a gap that research and browser-based labs can only partially close.
