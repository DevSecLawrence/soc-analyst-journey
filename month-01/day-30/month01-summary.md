# Month 1 Summary — 30 Days of SOC Analyst Training
 
**Date:** 2026-06-12
**Days completed:** 30
**GitHub commits:** 30+
**Standalone repos created:** 3
 
---
 
## What Month 1 Was
 
30 days ago I started a 180-day SOC analyst roadmap from scratch. No prior work experience. No bootcamp. Just a structured plan, a Kali VM, and daily commitment to showing up even when I didn't feel like it.
 
This is what that actually produced.
 
---
 
## Top 5 Things I Learned

**1. Incident report writing**
This surprised me more than anything technical. I always thought reporting was the boring part — it's not. Writing the same phishing incident three different ways for three different audiences (SOC manager, CISO, affected user) is a completely different skill from finding the incident in the first place. Most analysts can find the problem. Fewer can explain it to the right person in the right language.
 
**2. Malware analysis fundamentals**
YARA rules opened up a side of detection I hadn't thought about before — looking at what a file actually contains, not just what it does in logs. Understanding entropy, PE sections, and string matching changed how I think about what "detection" means.
 
**3. YARA rules**
Writing detection rules for files is harder than it looks. The specificity vs coverage problem is real — too tight and an attacker evades with one rename, too loose and you're flagging zip files all day. I wrote 3 rules from scratch, tested them in Kali, and actually understand the tradeoffs now.
 
**4. Sigma rules**
Portable detection logic that converts to any SIEM query language. This clicked for me when I realised Sigma is basically the "write once, run anywhere" of detection engineering. Wrote rules for PowerShell abuse, recon commands, and persistence — converted to Splunk SPL and Elastic KQL.

**5. Splunk**
Going from "I've heard of Splunk" to actually writing SPL queries, building detection logic, and understanding how a SIEM processes events was probably the biggest practical jump of the month. Not production experience, but I'm no longer starting from zero.
 
---
 
## Top 3 Things That Surprised Me
 
**1. How much writing matters**
I went into this thinking the technical work was the job. It's half the job. The other half is explaining what you found, to who, in what format. Day 25 — rewriting one incident three ways — was more cognitively demanding than any of the labs.
 
**2. Splunk's depth**
I knew it was widely used. I didn't know how deep it goes — the query language, the data pipeline, the way fields get extracted, the difference between a good detection and a noisy one. There's a lot under the surface and I've only scratched it.
 
**3. That I actually stayed consistent**
Genuinely didn't know if I'd make it through a full month alongside university coursework. Some days the roadmap got whatever hours were left after everything else. But I didn't miss a day. That surprised me more than any technical finding.
 
---
 