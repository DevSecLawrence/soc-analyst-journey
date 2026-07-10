# Day 41 — Data Exfiltration Patterns
 
**Date:** 2026-06-22
**MITRE Tactic:** TA0010 — Exfiltration
**Lab status:** Windows VM still down — research and detection writing only.
 
---
 
## Why Exfiltration is the Last Chance
 
By the time data is leaving the network, earlier defences have already failed. The attacker got in, established persistence, moved laterally, and found what they came for. Exfiltration is the final stage — and detecting it here is the difference between a contained incident and reading about your organisation in the news.
 
That's the brutal mentor framing and it's accurate. If you're catching an attack at the exfiltration stage you're already in a bad position. But catching it at the last stage is still infinitely better than not catching it at all.
 
The core problem with exfiltration detection: most exfiltration uses legitimate channels. HTTPS, DNS, email, cloud storage — these are things every organisation uses constantly. The attacker is hiding their data theft in the same traffic stream as normal business activity. Detection is almost never about the channel itself — it's about anomalies in how that channel is being used.
 
---
 
## The 5 Techniques
 
### 1. HTTP/HTTPS Exfiltration (T1048.003)
 
**How it works:**
The simplest approach — the attacker uploads data to an external server using HTTP POST requests or HTTPS uploads. Could be a file uploaded to a custom server, a web service, or even a legitimate file-sharing site.
 
**Why it's hard to detect:**
HTTPS encrypts the payload. Network inspection sees a connection to an IP or domain and the volume of data transferred, but not what the data is. Most organisations have enormous volumes of legitimate HTTPS traffic — an attacker's upload blends in easily.
 
**What network telemetry reveals it:**
- Large outbound data volumes to unusual destinations (high bytes transferred, low bytes received — upload pattern)
- Connections to newly registered domains or domains with no prior history in your environment
- Sustained uploads during non-business hours
- Beaconing pattern — regular connections at consistent intervals suggesting C2 communication alongside exfiltration
**Common tools used:**
curl, wget, PowerShell Invoke-WebRequest, custom Python scripts, legitimate cloud sync clients abused for the purpose
 
**What legitimate activity looks similar:**
Cloud backup software, software update checks, video calls, any SaaS platform that syncs data. The difference is volume pattern and destination — legitimate uploads go to known, consistent destinations; exfiltration goes somewhere new.
 
**Detection threshold:**
Alert on any single outbound connection that transfers more than [X] MB to a destination with no prior history in the environment. The threshold depends on baseline — which is why you need a baseline.
 
---
