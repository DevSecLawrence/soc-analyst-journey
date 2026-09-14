# Day 45 — Portfolio Audit

**Date:** 2026-07-15
**Total artifacts reviewed:** 44 days of work across month-01 and month-02

---

## 10 Strongest Artifacts

These are the pieces I'd point a recruiter to first,after my research — strongest combination of technical depth, documentation quality, and real investigative work:

### 1. BTLO Phishing Analysis — 10/10
**Location:** `month-01/day-24/`
**Why it's strong:** Real investigation, real score, documented methodology. Shows I can do the actual work not just read about it. The nested .eml attachment finding is technically specific and impressive.

### 2. LetsDefend Sysmon Attack Chain
**Location:** `month-01/day-23/`
**Why it's strong:** Full attack chain investigated — initial access, UAC bypass, persistence. All MITRE mapped. 757 events worked through. Shows investigation depth.

### 3. YARA Rules Collection
**Location:** `yara-rules-collection` repo
**Why it's strong:** Original rules, tested in Kali, limitations documented. Shows detection engineering, not just knowledge of the concept.

### 4. Sigma Rules Collection
**Location:** `sigma-rules-collection` repo
**Why it's strong:** Multiple rules, converted to SPL and KQL, ATT&CK mapped. Shows multi-SIEM thinking.

### 5. 3-Audience Incident Report
**Location:** `month-01/day-25/`
**Why it's strong:** Same incident, three completely different documents. Shows communication range — technical to executive to user. Rare skill at junior level.

### 6. BTLO Network Analysis — Web Shell
**Location:** `month-01/day-29/`
**Why it's strong:** Full PCAP investigation — port scan to reverse shell. Real hands-on Wireshark work with clear methodology.

### 7. Lateral Movement Detection — 5 Sigma Rules
**Location:** `month-02/day-40/`
**Why it's strong:** Detection logic for PSExec, WMI, WinRM, RDP, remote tasks. Shows understanding of the full lateral movement surface.

### 8. Persistence Mechanisms — 5 Sigma Rules
**Location:** `month-02/day-38/`
**Why it's strong:** Registry run keys, scheduled tasks, services, WMI subscriptions, startup folder — documented and detected. Relevant to every enterprise SOC.

### 9. Threat Hunting Hypotheses + Reports
**Location:** `month-02/day-42/`
**Why it's strong:** Structured hypothesis-driven hunting, not just searching. Two full hunt reports with query, false positive analysis, and refinement. Shows analyst thinking above Tier 1.

### 10. Month 1 Demo Reel
**Location:** `month-01/day-30/`
**Why it's strong:** Single-page showcase of everything. Useful for recruiters who won't browse 44 folders. The artifact that makes the rest of the portfolio accessible.

---

## 5 Artifacts That Need Improvement

### 1. Day 43 — AWS Fundamentals
**Issue:** No hands-on screenshots — lab account wasn't set up before the exams hit. Reads as research only. Need to complete the hands-on exercise and update with real screenshots.

### 2. Day 44 — Azure Fundamentals
**Issue:** Same as Day 43 — hands-on pending. The content is solid but without actual console screenshots it's theory not evidence.

### 3. Day 32 — EDR Fundamentals
**Issue:** Entirely conceptual — no hands-on with any actual EDR platform. Need to find a way to get at least basic exposure to Microsoft Defender for Endpoint.

### 4. Days 38-41 — Persistence/Lateral Movement/Exfil Sigma Rules
**Issue:** Rules are well-written but not tested — lab was down throughout. Need to rebuild the Windows VM, install Sysmon, and actually run these detections against simulated activity.

### 5. GitHub README — Progress Section
**Issue:** The progress bar and "currently working on" line hasn't been updated since Month 1. Needs to reflect Month 2 work and the current day count.

---

## Portfolio Gaps Not Yet Filled

| Gap | What's missing | How to fill it |
|-----|---------------|---------------|
| Active Directory | Nothing on AD attack/defence | TryHackMe AD rooms in Month 3 |
| Python security scripts | No working scripts | Write 3 scripts in Month 3 |
| EDR hands-on | No console screenshots | Microsoft Defender free trial |
| Cloud hands-on | No AWS/Azure screenshots | Complete Days 43-44 labs |
| CTF participation | No public CTF entries | BTLO investigations count — document them better |

---

## Overall Portfolio Health

**Strengths:**
- Consistent commit history — 44 days documented
- Three standalone showcase repos — professionally structured
- Real challenge completions with scores — not just labs
- Multi-format reporting — technical and executive and user

**Weaknesses:**
- Too many research-only days without hands-on evidence
- Windows VM lab being down for most of Month 2 limited practical work
- No Python scripts — a visible gap given how often it appears in JDs
- AWS and Azure labs incomplete — cloud section feels theoretical