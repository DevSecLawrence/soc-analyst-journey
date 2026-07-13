# Day 42 — Hunt Hypotheses
 
**Date:** 2026-06-23
**Environment:** Windows 10 endpoint + Kali Linux (local lab — VM currently down, queries pending rebuild)
 
---
 
## How to Read This Document
 
Each hypothesis follows the same structure:
- **Hypothesis** — the question being asked
- **Why it matters** — what real attack technique this covers
- **Data source** — where to look
- **Query approach** — what to search for
- **Success criteria** — what a positive finding looks like
- **False positive risk** — what legitimate activity might look the same
---
 
## Hypothesis 1 — Persistence via Scheduled Tasks Created Outside Business Hours
 
**Hypothesis:**
An attacker has established persistence by creating scheduled tasks outside of normal business hours, pointing to files in unusual locations.
 
**Why it matters:**
Scheduled tasks are a top persistence mechanism. Legitimate tasks are almost always created during business hours by known admin accounts or software installers. Tasks created at 2am by a standard user account are suspicious.
 
**Data source:**
Windows Security Event Log — Event ID 4698 (Scheduled Task Created)
 
**Query approach (Splunk SPL):**
```spl
index=windows EventCode=4698
| eval hour=strftime(_time, "%H")
| where hour < 6 OR hour > 22
| table _time, TaskName, SubjectUserName, TaskContent
| sort -_time
```
 
**Success criteria:**
Any Event ID 4698 outside 06:00–22:00 from a non-admin account or pointing to a file in `%TEMP%`, `%APPDATA%`, or `C:\Users\Public`.
 
**False positive risk:**
Legitimate backup software or scheduled maintenance tasks running overnight. Filter by known admin accounts and known task names to reduce noise.
 
---
