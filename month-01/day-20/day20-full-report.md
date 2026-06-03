# Malware Traffic Analysis — Incident Report
**Analyst:** Lawrence
**Date:** 2026-06-03
**PCAP:** 2020-09-25-traffic-analysis-exercise.pcap
**Classification:** Malware Infection — Payload Delivery
**Status:** Training Exercise

---

## Executive Summary

On 24 September 2020, a Windows workstation at
IP address 10.0.0.179 was observed downloading
a malicious executable named jojo.exe from an
external server at 198.12.66.108. The file is
a Windows PE binary (326KB) served over unencrypted
HTTP. Following the download, significant TLS
traffic was observed suggesting the host established
encrypted communication with attacker-controlled
infrastructure. The environment is an Active
Directory domain, raising the risk of lateral
movement. Immediate isolation of the affected
host and blocking of 198.12.66.108 at the
perimeter firewall is recommended.

---

## Technical Timeline

All times in UTC based on packet timestamps.
16:04:41 — Capture begins. Host 10.0.0.179
begins DNS resolution activity.
DNS server: 10.0.0.10.

![Protocol hierarchy showing protocols and byte distribution](./screenshots/Screenshot_2026-06-03_23_07_16.png)
*Protocol hierarchy — TLS and TCP dominate the capture.*

![Endpoints summary table (bytes / packets)](./screenshots/Screenshot_2026-06-03_23_08_34.png)
*Endpoints overview — internal host 10.0.0.179 and external 198.12.66.108 show heavy traffic.*
16:04:41 — DNS queries observed from 10.0.0.179
to internal DNS server. Multiple query
and response pairs.

![DNS queries captured in the PCAP (hex view)](./screenshots/Screenshot_2026-06-03_23_09_18.png)
*DNS queries — domain list needs clearer extraction.*
16:04:44 — HTTP GET request initiated:
10.0.0.179 → 198.12.66.108
GET /jojo.exe HTTP/1.1
User-Agent: Mozilla/4.0 (compatible;
Win32; WinHttpRequest.5)
       Note: WinHttpRequest user-agent is
       not a browser. This is a programmatic
       HTTP request — likely a downloader
       component already running on the host.
16:04:44 — Server 198.12.66.108 responds:
HTTP/1.1 200 OK
Server: Apache/2.4.6 (CentOS)
Content-Length: 326080
Content-Type: application/octet-stream
Response body begins with MZ header
— confirmed Windows PE executable.

![HTTP follow stream showing response headers and PE file header (MZ)](./screenshots/Screenshot_2026-06-03_23_10_00.png)
*Follow TCP stream — HTTP 200 serving a PE file (MZ header visible).*

![Packet list filtered for HTTP showing GET /jojo.exe](./screenshots/Screenshot_2026-06-03_23_11_03.png)
*Packet list — HTTP GET for jojo.exe.*
16:04:44 to 16:46:00 — Large volume TLS traffic
observed. 459 TLS packets, 1.54MB.
Likely C2 communication established
post-execution of jojo.exe.
       SMTP traffic (334 packets, 340KB)
       also observed — possible email delivery
       mechanism or post-infection spam.

       SMB2 traffic (126 packets) observed —
       possible lateral movement or legitimate
       Windows file sharing.

---

## IOCs Extracted

All values defanged for safe documentation.

**IP Addresses:**
198[.]12[.]66[.]108 — malicious server, served
jojo.exe — HIGH confidence
10[.]0[.]0[.]179    — infected host — HIGH confidence
10[.]0[.]0[.]10     — internal DNS server —
legitimate infrastructure

**URLs:**
hxxp://198[.]12[.]66[.]108/jojo[.]exe

**File:**
Filename:     jojo.exe
Size:         326,080 bytes (318KB)
Content-Type: application/octet-stream
Header:       MZ (Windows PE executable)
ETag:         4f9c0-5b01040d1a640
Last-Modified: Thu, 24 Sep 2020 14:45:37 GMT

**User-Agent (suspicious):**
Mozilla/4.0 (compatible; Win32; WinHttpRequest.5)
This is not a browser user-agent. WinHttpRequest
is a Windows scripting component used by malware
downloaders and legitimate automation tools.
Its presence indicates the HTTP request was made
programmatically, not by a user opening a browser.

---

## MITRE ATT&CK Mapping

| Technique ID | Name | Evidence |
|---|---|---|
| T1105 | Ingress Tool Transfer | jojo.exe downloaded from 198.12.66.108 via HTTP GET |
| T1071.001 | Application Layer Protocol: Web Protocols | HTTP used for payload delivery |
| T1071 | Application Layer Protocol | TLS traffic post-infection — likely C2 |
| T1204.002 | User Execution: Malicious File | PE executable downloaded and likely executed |
| T1021.002 | Remote Services: SMB/Windows Admin Shares | SMB2 traffic observed — possible lateral movement |
| T1018 | Remote System Discovery | LDAP queries suggest AD enumeration |
| T1558 | Steal or Forge Kerberos Tickets | Kerberos traffic in AD environment — worth monitoring |

---

## Confidence Assessment

**High confidence:**
- Host 10.0.0.179 downloaded a Windows PE
  executable named jojo.exe from 198.12.66.108
- The download used a programmatic user-agent,
  not a browser — this was not a user-initiated
  download
- 198.12.66.108 is malicious infrastructure

**Medium confidence:**
- TLS traffic post-download represents C2
  communication — plausible but unconfirmed
  without resolving destination IPs against
  threat intelligence
- The SMTP traffic is related to this infection —
  could be legitimate background email activity

**Low confidence:**
- The specific entry point for the infection
  (phishing email, drive-by download, exploit)
- Whether jojo.exe successfully executed or
  was caught by AV before execution
- Whether lateral movement was attempted or
  successful via SMB2

---

## Recommendations

**Immediate (within 1 hour):**
1. Isolate 10.0.0.179 from the network
2. Block 198.12.66.108 at perimeter firewall
   on all ports
3. Force password reset for all accounts that
   authenticated from 10.0.0.179

**Short term (within 24 hours):**
4. Submit jojo.exe hash to VirusTotal and
   Any.run for behavioral analysis
5. Search all other endpoints for connections
   to 198.12.66.108 — check if other hosts
   downloaded the same payload
6. Review SMTP logs — determine if the
   infection arrived via email
7. Check AD logs for unusual authentication
   from 10.0.0.179 — any accounts accessed
   that the user doesn't normally use

**Detection improvement:**
8. Create SIEM rule to alert on HTTP downloads
   of .exe files from external IPs
9. Create SIEM rule to alert on
   WinHttpRequest user-agent in proxy logs
10. Block or alert on direct IP HTTP connections
   — legitimate traffic uses domain names,
   not raw IPs

---

