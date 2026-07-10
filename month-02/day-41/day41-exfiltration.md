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
### 2. DNS Tunneling (T1071.004)
 
**How it works:**
DNS is one of the most universally allowed protocols — almost no network blocks outbound DNS queries. Attackers exploit this by encoding data inside DNS queries and responses. A query for `aGVsbG8gd29ybGQ.malicious.com` looks like a legitimate DNS lookup but the subdomain contains base64-encoded data. The attacker's DNS server receives it, decodes it, and responds with more encoded data.
 
**Why it's hard to detect:**
DNS traffic is everywhere and most organisations don't inspect it closely. The data is hidden in the query itself — in the subdomain portion — which gets forwarded transparently by your DNS resolver.
 
**What network telemetry reveals it:**
- High entropy subdomains — random-looking character strings like `xK9mQr2pL1nZ.domain.com` instead of readable names
- Unusually long DNS query strings — normal hostnames are short, tunneled data creates long subdomains
- High volume of DNS queries to a single domain
- DNS queries with unusually large response sizes (data coming back)
- Queries to domains that have never been seen in the environment before
**Detection approach:**
Entropy analysis on DNS subdomain strings. Normal subdomains have low entropy (readable words, predictable patterns). Tunneled data has high entropy (random-looking base64 or hex). Calculate Shannon entropy on the subdomain portion and alert on values above a threshold.
 
**Common tools used:**
dnscat2, iodine, DNSExfiltrator
 
**What legitimate activity looks similar:**
Some CDN services use long, encoded subdomains. Some tracking pixels and analytics use high-entropy subdomains. Legitimate use tends to be consistent and matches known service patterns. Tunneling tends to be unique per session.
 
---
### 3. Cloud Storage Abuse (T1567.002)
 
**How it works:**
The attacker uploads stolen data to a legitimate cloud storage service — Dropbox, OneDrive, Google Drive, Box. From a network perspective, the traffic looks completely normal because it IS going to a legitimate service. The data just isn't the attacker's data.
 
**Why it's hard to detect:**
You can't block Dropbox without blocking legitimate business use. The upload traffic is encrypted HTTPS to a known, legitimate domain. Content inspection isn't possible without SSL inspection infrastructure.
 
**What network telemetry reveals it:**
- Abnormally large uploads to cloud storage services from a machine that doesn't normally use them
- A machine that has never previously communicated with a cloud storage provider suddenly uploading hundreds of MB
- Multiple machines uploading to the same cloud storage account in sequence (post-lateral movement exfiltration)
- Uploads from machines that shouldn't have internet access (servers, kiosks)
**What legitimate activity looks similar:**
Literally every person who uses OneDrive, Dropbox, or Google Drive for work. This is why user behaviour baselining matters — an upload from an endpoint that normally uses OneDrive heavily is different from the same upload from a server that has never touched Dropbox before.
 
**Common tools used:**
Native cloud sync clients, rclone (popular exfil tool that supports dozens of cloud providers), custom scripts using cloud provider APIs
 
---
 