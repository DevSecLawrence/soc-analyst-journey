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

I anchored this section on MITRE T1048.003 to keep the HTTP/HTTPS exfil framing accurate.

![MITRE ATT&CK T1048.003 page used for HTTP/HTTPS exfiltration mapping](./screenshots/Screenshot%202026-07-10%20204630.png)
 
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

I used MITRE T1071.004 as the base reference for the DNS tunneling behavior.

![MITRE ATT&CK T1071.004 page used for DNS tunneling mapping](./screenshots/Screenshot%202026-07-10%20204645.png)
 
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

I also reviewed a Unit 42 write-up to cross-check practical DNS tunneling behavior beyond ATT&CK summary text.

![Unit 42 DNS tunneling research page used for practical detection context](./screenshots/Screenshot%202026-07-10%20204901.png)
 
**Common tools used:**
dnscat2, iodine, DNSExfiltrator
 
**What legitimate activity looks similar:**
Some CDN services use long, encoded subdomains. Some tracking pixels and analytics use high-entropy subdomains. Legitimate use tends to be consistent and matches known service patterns. Tunneling tends to be unique per session.
 
---
### 3. Cloud Storage Abuse (T1567.002)
 
**How it works:**
The attacker uploads stolen data to a legitimate cloud storage service — Dropbox, OneDrive, Google Drive, Box. From a network perspective, the traffic looks completely normal because it IS going to a legitimate service. The data just isn't the attacker's data.

I mapped this directly to MITRE T1567.002 for cloud storage exfiltration.

![MITRE ATT&CK T1567.002 page used for cloud storage exfiltration mapping](./screenshots/Screenshot%202026-07-10%20204702.png)
 
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
 ### 4. Email Exfiltration (T1048)
 
**How it works:**
The attacker sends data out via email — either as attachments to external addresses or encoded in the email body itself. If they have access to a compromised mail account, the traffic looks like normal email from a legitimate user.
 
**Why it's hard to detect:**
Sending email is legitimate behaviour for almost every user. A single large email with attachments is completely normal. The attack is only visible in the pattern or destination.
 
**What network telemetry reveals it:**
- Large email attachments sent to external addresses not in the organisation's contact history
- Multiple emails sent to the same external address in rapid succession
- Emails sent to personal email domains (gmail.com, yahoo.com) from corporate accounts — especially from accounts that don't normally do this
- Emails sent outside business hours
- SMTP connections from machines that don't normally send email (servers, internal systems)
**DLP (Data Loss Prevention) is the primary control here:**
Email DLP rules that flag attachments containing credit card numbers, SSNs, source code patterns, or large volumes of any structured data type. Content inspection is possible because email is often inspected by the email gateway.
 
**Common tools used:**
Native email client, PowerShell Send-MailMessage, SMTP scripts, compromised webmail accounts
 
---
 ### 5. Protocol Tunneling / Alternate Channels (T1048.001)
 
**How it works:**
Attackers use protocols that aren't normally used for data transfer to carry exfiltrated data. ICMP (ping) can carry data in the payload field. Other examples include encoding data in HTTP headers, using IRC, or tunneling over HTTPS to non-standard ports.

I referenced the parent ATT&CK technique T1048 here because this section is about alternate protocol channels as a whole.

![MITRE ATT&CK T1048 page used for alternate protocol exfiltration mapping](./screenshots/Screenshot%202026-07-10%20204715.png)
 
**Why it's hard to detect:**
These protocols are either always allowed (ICMP) or look like normal traffic from the outside (HTTPS on non-standard port might look like a developer tool or VPN).
 
**What network telemetry reveals it:**
- ICMP packets with unusually large payloads — normal pings are tiny, ICMP tunneling pings are large
- Outbound connections on unusual ports that don't match any known application
- HTTPS traffic to non-443 ports (could indicate tunneling or C2)
- Any protocol showing consistent, regular communication that doesn't match known application behaviour
**Common tools used:**
ptunnel (ICMP tunneling), nping, custom scripts encoding data in protocol fields
 
---
 
## The Hard Truth About Exfiltration Detection
 
All five of these techniques share one problem: they use legitimate channels. There's no "exfiltration protocol" that you can simply block. Detection requires:
 
1. **A baseline** — you can't spot anomalies without knowing what normal looks like
2. **Behavioural analysis** — looking at patterns over time, not just individual packets
3. **Correlation** — combining endpoint alerts (a compromised machine) with network anomalies (unusual uploads from that machine)
If you only detect at the network level, you'll miss encrypted exfiltration. If you only detect at the endpoint level, you'll miss exfiltration via legitimate tools. The combination is what gives you coverage.
 
---
 
## What I Concluded
 
Exfiltration is the hardest stage to detect because it's the most legitimate-looking. An attacker uploading to Dropbox looks exactly like an employee backing up their files. The only difference is context — which machine, which account, what time, what volume, what destination. None of that is visible in any single packet or log entry. It requires stitching together endpoint telemetry, network flows, and user behaviour over time.
 
The detection approach that makes most sense to me is layered: alert on large outbound volume anomalies from the network, correlate with endpoint telemetry showing which process created the traffic, and cross-reference with any prior alerts on that machine or user. Exfiltration caught in isolation looks like noise. Exfiltration in the context of a known compromised machine looks like an incident.
 
---
 
## Assumption I Made
 
I assumed that HTTPS encryption made exfiltration via web channels essentially undetectable. It makes content inspection impossible, but metadata is still visible — destination IP/domain, volume transferred, timing, frequency. A machine that uploads 2GB to a domain it has never communicated with before at 3am is detectable even if the content is encrypted. The content is invisible but the behaviour is not.
 
---
 
## Uncertainty I Have
 
I don't know how to set meaningful volume thresholds without historical baselines. How much outbound traffic is normal for a machine in my environment? Without knowing that number, any threshold I set is a guess — too low and I'm drowning in false positives from cloud backup software, too high and I'm missing real exfiltration. Building that baseline is a weeks-long process and I don't have a framework yet for doing it systematically. This is something I need to understand better before I could deploy any of these detections in a real environment.