# Day 37 — Living Off the Land: LOLBAS Techniques

**Date:** 2026-06-28
**Resource:** lolbas-project.github.io
**Lab testing:** Windows host (safe commands only — no malware downloads)

---

## What I Did

Spent today on LOLBAS — Living Off the Land Binaries and Scripts. The concept is simple: attackers use tools that are already installed on Windows instead of bringing their own malware. The tools are legitimate, signed by Microsoft, and trusted by antivirus. The abuse is in how they're used.

I went through lolbas-project.github.io and researched 10 binaries. Then I tested 5 of them on my Windows host using harmless arguments just to see what the process trees and command lines look like — without downloading anything malicious. Wrote Sigma detection rules for each.

Before today I kind of understood LOLBins conceptually. After going through each binary properly — what it's supposed to do, what attackers do with it, what the command line looks like when it's being abused — I understand why this technique is so effective. The binary is trusted. The signature is valid. The only thing that gives it away is context: what arguments it's running with, what process spawned it, and whether it makes a network connection it shouldn't.

---

## What I Concluded

You can't block LOLBAS binaries. certutil.exe is a real certificate utility that gets used legitimately. mshta.exe runs real HTML applications. regsvr32.exe registers real DLLs. Blocking them would break things.

The detection has to be contextual. The questions are:
- Is this binary being run by a process that would normally use it?
- Are the command line arguments in line with legitimate use?
- Is it making a network connection it shouldn't?
- Is it running from an unusual location or user context?

That's a harder detection problem than "block bad file hash" — and it's why LOLBAS techniques are so common in real attacks. The initial access gets blocked. The attacker pivots to tools that are already there.

The other thing that hit me: LOLBAS detection is exactly what the Sigma rules and process tree analysis from Days 35 and 36 were building toward. The parent process context, the command line arguments, the network connections from unexpected processes — all of that becomes the detection layer when the binary itself looks clean.

## Screenshot Evidence

![LOLBAS project homepage used as the source for binary abuse research and ATT&CK mappings](./screenshots/Screenshot%202026-06-29%20212851.png)

---

## Assumption I Made

I assumed that unusual parent processes were the main detection signal for LOLBAS abuse. After going through each binary properly I realised command line arguments are often a stronger signal. certutil downloading a file from an IP address rather than a certificate authority URL is suspicious regardless of what spawned it. The argument tells you the intent even when the parent looks clean.

---

## Uncertainty I Have

I don't know how to handle environments where IT admins legitimately use these binaries for automation. A sysadmin using certutil to distribute certificates across the network will generate the same kind of alerts as an attacker using certutil to stage malware. The detection logic is the same — the intent is completely different. Reducing false positives in that scenario requires knowing what normal admin behaviour looks like in that specific environment, which means baselining. That's something I can't do without being inside a real organisation's network.