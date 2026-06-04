# Day 21 — Sigma Conversion Comparison

Purpose: Compare Sigma conversion output to Splunk SPL and Elastic KQL, and document field mapping issues.

## Summary
Sigma conversion works, but it is not clean. It gives you a usable starting point, then you still have to fix field names and tune conditions to match your log source.

## Conversion Results

### Rule 1 — whoami.exe execution
- Sigma file:
- Splunk SPL:
- Elastic KQL:
- Notes: Splunk conversion ran successfully from the `sigma-rules` folder. Output still needs field name validation against your event IDs/logs.

### Rule 2 — PowerShell encoded command
- Sigma file:
- Splunk SPL:
- Elastic KQL:
- Notes: Not converted yet. This rule will need careful field mapping for `CommandLine` vs `process.command_line` depending on the platform.

### Rule 3 — New local admin account creation
- Sigma file:
- Splunk SPL:
- Elastic KQL:
- Notes: Needs cleanup first (the file currently has two rules). After split, convert each separately.

## Field Mapping Issues

- `Image` vs `process_path` vs `process.executable`
- `CommandLine` vs `process.command_line`
- `EventID` field naming differences (WinEventLog vs Sysmon)
- Process creation category vs Security log events (4688 vs 4720/4732)
