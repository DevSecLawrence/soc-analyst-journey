# Day 20 — Network Traffic Analysis: PCAP Investigation

**File:** 2020-09-25-traffic-analysis-exercise.pcap
**Source:** malware-traffic-analysis.net

---

## What I Concluded

The PCAP shows a single Windows host getting
infected and downloading a malicious executable
over plain HTTP from an external server.

The infected host is 10.0.0.179 — an ASUS machine
on what looks like a corporate Active Directory
network. I can tell it's AD because Kerberos, LDAP,
and SMB2 traffic are all present. Those protocols
don't show up on home networks.

The most significant thing I found was in the HTTP
stream. The host made a GET request for /jojo.exe
to 198.12.66.108. The server responded with HTTP
200 OK and delivered a 326KB file. The response
body starts with MZ — that's the Windows PE
executable header. This host downloaded and likely
executed a malicious binary.

The TLS traffic at 11.6% of packets and 60.8%
of bytes is disproportionately large. After a
malware download you'd expect to see C2 traffic
— encrypted communication back to attacker
infrastructure. That TLS volume is consistent
with an established C2 channel.

The SMTP traffic at 8.5% is interesting. It could
be the initial delivery mechanism — a malicious
email that triggered the download — or post-
infection spam activity from the compromised host.

---

## Answering the 3 Medium Questions

**1. What hosts are involved?**
- 10.0.0.179 — infected Windows host (ASUSTekCOMPU)
- 10.0.0.10 — internal DNS server
- 198.12.66.108 — external malicious server
  (served jojo.exe)
- Multiple other external IPs visible in TLS
  traffic — likely C2 infrastructure

**2. What protocols are used?**
- TCP: 94.2% — dominant
- TLS: 11.6% — encrypted traffic, likely C2
- SMTP: 8.5% — email traffic
- SMB2: 3.2% — file sharing / lateral movement
- DNS: 2.5% — name resolution
- Kerberos: 0.3% — AD authentication
- LDAP: 1.3% — directory queries
- HTTP: 0.1% — only 2 packets, but they're the
  most important ones in the whole capture

**3. What is the likely scenario?**
Malware infection with payload delivery over HTTP
followed by encrypted C2 communication. The
presence of Kerberos and LDAP suggests the attacker
may be attempting to move laterally or enumerate
the Active Directory environment post-infection.

---

## Assumption I Made

I assumed the large TLS traffic was C2 because
it appeared after the jojo.exe download. But TLS
traffic can also be legitimate — background Windows
update traffic, telemetry, certificate checks. I
can't confirm C2 from TLS alone without resolving
the destination IPs and checking them against
threat intelligence. I treated it as suspicious
based on volume and timing, but I documented the
uncertainty rather than calling it confirmed.

## Uncertainty I Have

I could not read the DNS queries clearly enough
from the screenshots to know exactly what domains
were queried before the HTTP download. Those DNS
queries are the first indicator — they would tell
me whether the host was directed to 198.12.66.108
by a malicious domain or contacted it by IP directly.
Getting the full domain list from the DNS filter
would complete the picture.

I also don't know what jojo.exe actually does
beyond the fact that it's a Windows PE executable.
Submitting it to Any.run or VirusTotal would give
me behavioral analysis — what processes it spawns,
what registry keys it creates, what C2 it calls
home to.

## Comparison to Solution

I identified the core infection correctly:
- Infected host: 10.0.0.179 ✅
- Malicious server: 198.12.66.108 ✅
- Payload: jojo.exe downloaded over HTTP ✅
- Environment: Active Directory corporate network ✅

What I likely missed based on the protocol mix:
- The specific DNS domains queried before infection
- Whether the SMTP traffic was inbound (delivery)
  or outbound (post-infection spam)
- Any persistence mechanisms established after
  jojo.exe executed
- Secondary payload downloads that may have
  happened over TLS and weren't visible as HTTP