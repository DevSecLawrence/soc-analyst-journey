# Hunt Report 1 — Scheduled Task Persistence Outside Business Hours

**Hunt date:** 2026-06-23
**Analyst:** Lawrence
**Hypothesis:** An attacker has established persistence via scheduled tasks created outside business hours
**Status:** Research-based — lab rebuild pending. Query designed and documented, execution pending.

---

## Hypothesis

"If an attacker has established persistence via scheduled tasks, they likely created those tasks outside of normal business hours to avoid detection, and the task will point to a file in an unusual location like %TEMP% or %APPDATA%."

---

## Data Source

Windows Security Event Log — Event ID 4698 (A scheduled task was created)

**Why this data source:**
Event ID 4698 fires every time a scheduled task is created and includes the task name, the creating account, and the full task XML showing what the task runs. This gives us everything we need to evaluate whether a task is legitimate or suspicious.

**Telemetry gap to note:**
Event ID 4698 only fires if "Audit Other Object Access Events" is enabled in Group Policy. Without this audit policy configured, scheduled task creation is invisible in the Security log. This is a common gap in many environments.

---

## Query (Splunk SPL)

```spl
index=windows EventCode=4698
| eval hour=strftime(_time, "%H")
| where hour < 6 OR hour > 22
| rex field=TaskContent "(?i)<Command>(?P<command>[^<]+)</Command>"
| where command LIKE "%Temp%" 
    OR command LIKE "%AppData%" 
    OR command LIKE "%Public%"
    OR command LIKE "%.ps1%"
    OR command LIKE "%-enc%"
| table _time, SubjectUserName, TaskName, command
| sort -_time
```

---

## Expected Results

**If the hunt finds nothing:**
No scheduled tasks created outside business hours pointing to suspicious locations. This is the expected result in a clean environment and confirms absence of this specific persistence technique. Still valuable — rules out this vector.

**If the hunt finds something suspicious:**
A task created at an unusual hour by a standard user account pointing to a file in `%TEMP%` or containing base64 encoded PowerShell. This would be a high-confidence finding warranting immediate investigation.

---

## False Positive Analysis

| Finding type | Likely explanation | How to filter |
|-------------|------------------|---------------|
| Task created at 2am by SYSTEM | Legitimate Windows maintenance | Filter SubjectUserName = "SYSTEM" |
| Task created by known admin at 11pm | Late-night admin work | Whitelist known admin accounts |
| Task pointing to Program Files | Software installer ran overnight | Filter by known installer paths |

---

## Refinement

After removing SYSTEM-created tasks and known admin accounts, the remaining set should be small enough to manually review. Any task with an unusual creator + unusual time + unusual file path combination is worth escalating.

---

## Hunt Outcome

**Pending lab rebuild.** Query is designed and false positive filtering is planned. Will execute and update this report when the Windows VM is operational.

---

## Lessons from Designing This Hunt

The hardest part was the false positive problem — a task created at 2am by the SYSTEM account is completely normal. Without filtering that out first, the query would return hundreds of legitimate results and bury any real finding. Hunt query design is as much about excluding the known-good as it is about finding the suspicious.
