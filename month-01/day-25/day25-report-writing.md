# Day 25 — Report Writing
 
**Date:** 2026-06-08
**Based on:** Day 24 phishing investigation (BTLO Phishing Analysis)
 
---

## What I Did
 
Took the same phishing incident from yesterday and rewrote it three times for three completely different audiences:
 
1. **Technical report for SOC manager** — full detail, IOC table, MITRE mapping, confidence levels, timeline
2. **Executive summary for CISO** — one paragraph, no jargon, business impact, clear action items
3. **Email to the affected user** — three sentences, plain English, no blame, asks one specific question
Same facts. Completely different language, structure, and length each time.
 
---

## What I Concluded
 
Writing is not a soft skill in security — it's a core skill. Finding an incident is only half the job. If you can't explain it clearly to the right person in the right language, the finding is useless. The CISO doesn't need to know what base64 encoding is. The affected user doesn't need a MITRE ATT&CK reference. The SOC manager needs both.
 
The hardest version to write was the executive summary — not because it's long, but because it has to be complete in one paragraph. Every word has to earn its place. I had to strip out everything technical without stripping out the meaning. That's harder than writing 2 pages.
 
The user email was harder than it looked too. You have to be honest about what happened, reassuring enough that they don't panic, and still get the information you need — all in 3 sentences. Tone matters as much as content there.
 
---

## Assumption I Made
 
I assumed more technical detail meant a better report. It doesn't — it means a better report for one specific audience. Dumping IOC tables and MITRE IDs into an executive summary doesn't show competence, it shows you don't understand who you're writing for. The skill is knowing what to include and what to cut for each audience.
 
---
 