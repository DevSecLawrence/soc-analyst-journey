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

## Screenshot Evidence

![MITRE ATT&CK T1003.001 page for LSASS Memory credential dumping](./screenshots/Screenshot%202026-07-07%20234159.png)

![MITRE ATT&CK T1003.002 page for SAM credential dumping](./screenshots/Screenshot%202026-07-07%20234252.png)

![ADSecurity reference page for Mimikatz and Active Directory Kerberos attacks](./screenshots/Screenshot%202026-07-07%20234314.png)

![Microsoft Learn Credential Guard overview used for protection controls](./screenshots/Screenshot%202026-07-07%20234344.png)

![Microsoft Learn Configure added LSA protection page used for LSASS hardening guidance](./screenshots/Screenshot%202026-07-07%20234404.png)
 
---

## Assumption I Made
 
I assumed Kerberoasting required special tools or elevated privileges. It doesn't — any authenticated domain user can request service tickets for any SPN in the domain. That's by design. The protocol was built that way. Kerberoasting abuses a legitimate feature, not a vulnerability. That makes it harder to prevent at the protocol level and harder to detect because the ticket requests themselves look completely normal — it's only the volume, the timing, and the encryption type that give it away.
 
---
 
## Uncertainty I Have
 
I don't fully understand how to detect Kerberoasting without access to domain controller logs. Event ID 4769 only fires on the domain controller, not on the machine running the attack. In an environment where I'm a tier 1 analyst without DC log access, I might never see the Kerberoasting attempt in my SIEM. I need to understand what the SOC visibility model looks like for DC logs — who has access, how they're forwarded, and what the latency is — before I can say I can actually detect Kerberoasting in practice.