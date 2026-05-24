# Day 11 - Severity Reference

## Syslog Severity Levels

- 0: Emergency
- 1: Alert
- 2: Critical
- 3: Error
- 4: Warning
- 5: Notice
- 6: Informational
- 7: Debug

## Notes

# Syslog Severity and Facility Reference

## How PRI is Calculated

PRI = (Facility × 8) + Severity

Every syslog message starts with a PRI value in angle brackets
e.g. <14> means facility 1 (user) × 8 + 6 (info) = 14

---

## Severity Levels (0-7)

| Number | Name    | Meaning                        | Real example                        |
|--------|---------|--------------------------------|-------------------------------------|
| 0      | emerg   | System is unusable             | Kernel panic, complete failure      |
| 1      | alert   | Immediate action needed        | Database corruption detected        |
| 2      | crit    | Critical condition             | Hard drive failure imminent         |
| 3      | err     | Error condition                | Service failed to start             |
| 4      | warning | Warning — not broken yet       | Disk space above 80%                |
| 5      | notice  | Normal but worth noting        | User logged in outside hours        |
| 6      | info    | Informational                  | Service started successfully        |
| 7      | debug   | Debug detail                   | Variable values during testing      |

---

## Common Facility Numbers

| Number | Name    | Source                          |
|--------|---------|---------------------------------|
| 0      | kern    | Linux kernel                    |
| 1      | user    | User-level programs             |
| 2      | mail    | Mail system                     |
| 3      | daemon  | System daemons                  |
| 4      | auth    | Authentication (login, sudo)    |
| 5      | syslog  | rsyslog internal messages       |
| 16     | local0  | Custom use — often network gear |
| 17     | local1  | Custom use                      |
| 23     | local7  | Custom use                      |

---

## PRI Calculation Examples

| Facility | Severity | Calculation  | PRI |
|----------|----------|--------------|-----|
| user (1) | emerg (0)| 1×8 + 0      | 8   |
| user (1) | alert (1)| 1×8 + 1      | 9   |
| user (1) | crit (2) | 1×8 + 2      | 10  |
| user (1) | err (3)  | 1×8 + 3      | 11  |
| user (1) | warning (4)| 1×8 + 4    | 12  |
| user (1) | notice (5)| 1×8 + 5     | 13  |
| user (1) | info (6) | 1×8 + 6      | 14  |
| user (1) | debug (7)| 1×8 + 7      | 15  |
| kern (0) | emerg (0)| 0×8 + 0      | 0   |
| auth (4) | notice (5)| 4×8 + 5     | 37  |

---

## SOC Relevance

In a SIEM, severity 0-2 should auto-create alerts.
Severity 3-4 should be reviewed daily.
Severity 5-6 is your baseline noise — useful for context.
Severity 7 (debug) is usually filtered out at ingestion
to reduce storage costs — if you need it you enable it
per-source temporarily during an investigation.
