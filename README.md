# SOC Analyst Journey — 180 Days

I'm Lawrence. I'm teaching myself to become a SOC analyst through a structured 180-day roadmap — daily labs, real investigations, and everything documented publicly. No bootcamp, no paid course, just consistent work and honest documentation.

This repo is my proof of work. Every day has a write-up, artifacts, and my actual reasoning — including where I got stuck, what I got wrong, and what I still don't understand. I'm not trying to look perfect. I'm trying to get good.

**Currently working on:** Month 1 — Foundations

---

![Kali Linux](https://img.shields.io/badge/Kali_Linux-557C94?style=flat&logo=kalilinux&logoColor=white)
![Wireshark](https://img.shields.io/badge/Wireshark-1679A7?style=flat&logo=wireshark&logoColor=white)
![Splunk](https://img.shields.io/badge/Splunk-000000?style=flat&logo=splunk&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat&logo=linux&logoColor=black)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)
![VS Code](https://img.shields.io/badge/VS_Code-007ACC?style=flat&logo=visualstudiocode&logoColor=white)

---

## Skills Demonstrated So Far

| Skill | Tools |
|-------|-------|
| Packet analysis & protocol investigation | Wireshark |
| Windows Event Log & log analysis | Event Viewer, auditd |
| MITRE ATT&CK framework mapping | attack.mitre.org |
| SIEM threat hunting | Splunk, SPL, KQL |
| Detection rule writing | Sigma, YARA |
| Malware pattern matching | YARA 4.5.5, UPX |
| Detection lab setup & endpoint logging | Sysmon, VirtualBox, Kali |
| Phishing email investigation & IOC collection | VS Code, url2png, whois |
| Incident report writing (3 audiences) | Markdown |

---

## Featured Projects

### [YARA Rules Collection](https://github.com/DevSecLawrence/yara-rules-collection)
3 original YARA rules written and tested in Kali Linux — suspicious string detection, high entropy flagging, and UPX PE section detection. Includes the `.yar` files, test methodology, and known limitations for each rule.

### [Sigma Rules Collection](https://github.com/DevSecLawrence/sigma-rules-collection)
Original Sigma detection rules with full documentation — ATT&CK mappings, false positive analysis, and converted SPL/KQL queries. Covers PowerShell execution, recon commands, and persistence techniques.

### [Incident Reports](https://github.com/DevSecLawrence/incident-reports)
Real investigation write-ups from hands-on challenges — phishing email analysis (BTLO, 10/10), Sysmon attack investigation (LetsDefend), and professional reports written for three different audiences: SOC manager, CISO, and affected user.

---

## Progress

| Month | Focus | Status |
|-------|-------|--------|
| [Month 1](./month-01/) | Foundations — packets, logs, SIEM, detection rules, lab setup | 🟡 In progress |
| Month 2 | Threat intelligence, malware analysis, network forensics | 🟡 In progress |
| Month 3 | Incident response, digital forensics, memory analysis | ⬜ Not started |
| Month 4 | Cloud security, Active Directory attacks, advanced SIEM | ⬜ Not started |
| Month 5 | Red team fundamentals, CTF challenges, detection gaps | ⬜ Not started |
| Month 6 | Job preparation, capstone investigation, portfolio review | ⬜ Not started |

---

## Month 1 — Foundations

| Week | Days | Topics |
|------|------|--------|
| Week 1 | 1–7 | OSI model, packet analysis, Wireshark, PCAP investigation |
| Week 2 | 8–14 | Windows Event Logs, log correlation, authentication analysis |
| Week 3 | 15–21 | MITRE ATT&CK, Splunk SPL, Sigma rules |
| Week 4 | 22–30 | YARA rules, detection lab, phishing analysis, report writing, GitHub portfolio |

---

## Repo Structure
Example layout (files appear as work is completed):

```text
month-01/
  day-01/
    day01-osi-analysis.md
    pcap-samples/
      day01-normal traffic.pcapng
      day01-layer1-failure.pcapng
      day01-layer3-failure.pcapng
      day01-layer7-failure.pcapng
  day-02/
    ...
month-02/
  ...
```

## How Each Day Is Documented

Every day folder contains:

- A markdown write-up with what I did, what I found, and what I concluded
- Supporting artifacts — PCAPs, rule files, screenshots, log samples
- Three analyst prompts answered honestly:
  - **What I Concluded** — the main takeaway
  - **Assumption I Made** — something I got wrong or oversimplified
  - **Uncertainty I Have** — what I still don't fully understand

I write these in my own words. No polishing, no pretending I understood everything first time.

---

## Setbacks (Documented Honestly)

- **Day 23** — Accidentally formatted the external drive that had the Windows 10 VM and ISO on it. Lost the lab setup mid-build. Pivoted to LetsDefend browser-based lab instead of stopping. Local lab rebuild is pending.
- **Day 24 (roadmap)** — Atomic Red Team requires a local Windows VM. Skipped for now, will revisit when lab is rebuilt.

---

## Safety and Scope

All activity is local and controlled. No external targeting. No real credentials or sensitive data in any artifacts. PCAP samples contain only controlled traffic generated in isolated lab environments.

---

## Connect

- **LinkedIn:** [Okoli Chiemerie Lawrence](https://www.linkedin.com/in/okoli-chiemerie-lawrence-552415377/)
- **X:** [@only_Lawrence](https://x.com/only_lawrence)
- **GitHub:** [github.com/DevSecLawrence](https://github.com/DevSecLawrence)








