# Day 46 — Security+ SY0-701 Exam Objectives: Mapped to My Current Knowledge

**Date:** 2026-07-15
**Source:** Official CompTIA SY0-701 Exam Objectives PDF

---

## Domain 1 — General Security Concepts (12%)

| Sub-objective | My rating | Roadmap coverage |
|--------------|-----------|-----------------|
| 1.1 Security controls categories | 2/5 | Partial — know technical controls, weak on administrative/physical |
| 1.2 Fundamental security concepts (CIA, AAA, zero trust) | 3/5 | CIA covered, zero trust mentioned but not deep |
| 1.3 Change management security impact | 1/5 | Not covered |
| 1.4 Cryptographic solutions | 1/5 | Know what encryption is, not implementation details |

**Biggest gap:** Cryptography. RSA, ECC, AES, hashing algorithms, PKI, certificates — the exam goes deep here and I haven't.

---

## Domain 2 — Threats, Vulnerabilities, and Mitigations (22%)

| Sub-objective | My rating | Roadmap coverage |
|--------------|-----------|-----------------|
| 2.1 Threat actors and motivations | 3/5 | MITRE work covers this |
| 2.2 Threat vectors and attack surfaces | 3/5 | Phishing, lateral movement, exfiltration covered |
| 2.3 Vulnerability types | 2/5 | Basic understanding, not exam-depth |
| 2.4 Indicators of malicious activity | 4/5 | Strongest area — YARA, Sigma, Sysmon work |
| 2.5 Mitigation techniques | 3/5 | Detection and response covered, prevention less so |

**Biggest gap:** Vulnerability management specifics — CVSS scoring, CVE lifecycle, patch management processes.

---

## Domain 3 — Security Architecture (18%)

| Sub-objective | My rating | Roadmap coverage |
|--------------|-----------|-----------------|
| 3.1 Security implications of architecture models | 2/5 | Cloud covered at concept level |
| 3.2 Enterprise infrastructure security | 2/5 | Basic networking, VPC/NSG covered |
| 3.3 Data protection | 1/5 | Not covered |
| 3.4 Resilience and recovery | 1/5 | Not covered |
| 3.5 Security implications of cloud | 2/5 | AWS/Azure fundamentals from Days 43-44 |

**Biggest gap:** Data protection concepts (DLP, classification, encryption at rest/transit) and resilience/recovery (BCDR, RPO, RTO).

---

## Domain 4 — Security Operations (28%)

| Sub-objective | My rating | Roadmap coverage |
|--------------|-----------|-----------------|
| 4.1 Common security techniques | 3/5 | Log analysis, monitoring covered well |
| 4.2 Threat intelligence | 3/5 | MITRE ATT&CK used throughout |
| 4.3 Vulnerability management | 2/5 | Basic concepts only |
| 4.4 Alerting and monitoring | 4/5 | SIEM, EDR, Sysmon all covered |
| 4.5 Modify enterprise capabilities | 2/5 | Detection engineering covered, enterprise hardening less so |
| 4.6 Implement and maintain identity | 2/5 | IAM basics from AWS/Azure days |
| 4.7 Automate and orchestrate security | 1/5 | Not covered — SOAR, playbooks |
| 4.8 Incident response | 4/5 | Strong — investigation methodology, reporting all covered |
| 4.9 Data sources for investigations | 4/5 | CloudTrail, Sysmon, Windows Event Logs all covered |

**This is my strongest domain.** 28% of the exam and the roadmap covers most of it.

---

## Domain 5 — Security Program Management and Oversight (20%)

| Sub-objective | My rating | Roadmap coverage |
|--------------|-----------|-----------------|
| 5.1 Summarize governance elements | 1/5 | Not covered |
| 5.2 Risk management | 1/5 | Know the concept, not ALE/SLE/ARO calculations |
| 5.3 Third-party risk assessment | 1/5 | Not covered |
| 5.4 Data compliance and privacy | 1/5 | Know GDPR/HIPAA/PCI DSS names, not specifics |
| 5.5 Audit and assessment | 1/5 | Not covered |

**This is my weakest domain.** 20% of the exam and I've barely touched any of it. Governance, risk calculations, compliance frameworks, policy development — all need dedicated study.

---

## My Knowledge Distribution

```
Domain 1 (12%): ██░░░░░░░░  ~20% ready
Domain 2 (22%): █████░░░░░  ~50% ready  
Domain 3 (18%): ███░░░░░░░  ~30% ready
Domain 4 (28%): ███████░░░  ~70% ready
Domain 5 (20%): █░░░░░░░░░  ~10% ready

Weighted estimate: ~40% exam-ready currently
Practice test result: 57% — slightly above estimate, good sign
```