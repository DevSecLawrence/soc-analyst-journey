# Day 20 — Full Analysis Report

Case Info
---------
- Case ID: DAY20-PCAP-EXERCISE
- Source: malware-traffic-analysis.net (exercise name)
- Priority: Medium

---

## Executive Summary

- One-paragraph non-technical summary for management: what happened, impact, and recommended immediate action.

---

## Technical Timeline

- Chronological list of observable events from the PCAP (timestamped): DNS → HTTP/TLS → payload download → callback

---

## IOCs

- See `day20-iocs.csv` for machine-readable IOCs. Summarize the key indicators here.

| Type | Value |
|---|---|
| IP | 1.2.3.4 |
| Domain | bad-domain[.]example |
| Hash | abcdef123456... |

---

## ATT&CK Mapping

- Map high-level behaviors to MITRE ATT&CK techniques (e.g., T1071.001 - Web Protocols for C2 over HTTP).

---

## Confidence Assessment

- Describe sources of certainty vs assumptions (e.g., sample contains payload download but no persistence evidence in PCAP).

---

## Recommendations

- Containment: block IPs/domains at perimeter, remove artifacts from affected hosts.
- Detection: add signatures/rules (Suricata/Zeek/KQL) with tuning notes.
- Remediation: suggested EDR hunts and endpoint checks.

---

## Evidence

Place screenshots from `screenshots/` here. Example:

![PCAP Protocol Hierarchy](./screenshots/pcap-overview.png)

(Redact internal hostnames/IPs before publishing.)
