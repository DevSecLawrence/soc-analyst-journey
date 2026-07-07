# Day 39 — Credential Access and Protection
 
**Date:** 2026-07-07
**MITRE Tactic:** TA0006 — Credential Access
 
---
 
## What I Did
 
Researched 5 credential theft techniques — LSASS dumping, SAM extraction, Credential Manager access, Kerberoasting, and browser credential theft. For each one I documented how it works, what telemetry catches it, and what protections exist. No hands-on lab today — Windows VM still down.
 
---
 
## What I Concluded
 
Credential theft is what turns a limited foothold into full domain compromise. An attacker who gets onto one machine with low privileges can dump LSASS or run Kerberoasting and come out with domain admin credentials — without ever exploiting another vulnerability. They just authenticate normally from that point on.
 
That's the scary part. Once credentials are stolen, the attacker looks legitimate to every authentication system in the environment. No exploit. No malware signature to detect. Just valid credentials being used, possibly from a new location or at an unusual time.
 
This is why credential protection (Credential Guard, PPL, LAPS, strong passwords on service accounts) is just as important as detection. Detection catches the theft attempt. Protection stops it from succeeding even if the attempt happens.
 
The other thing that hit me: browser credential theft is massively underestimated. People save their work passwords in Chrome without thinking twice. Chrome encrypts those passwords with DPAPI — which means any process running as that user can decrypt them. No privilege escalation required. If a user opens a malicious email attachment and the malware runs as their user account, it can vacuum up every saved browser password in seconds.
 
---

