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
 
 ## Uncertainty I Have
 
I don't know how to calibrate confidence levels properly yet. I wrote "High" for the malicious URL and "Unknown" for payload delivery — but I don't have a standard framework for what High, Medium, and Low actually mean in a real SOC environment. Different organisations use different scales and different thresholds. I need to find out what the standard is before I write a real report with those labels.
 
---
 
## Why This Day Matters
 
Every analyst I've read about who moves up — into threat intel, detection engineering, incident response leadership — talks about writing. Not code, not tools, writing. The ability to explain a technical finding to a non-technical executive in plain English is rare. Most people coming up through security are technical first and communicators second, if at all. This is the skill that separates analysts who stay at Tier 1 from the ones who don't.