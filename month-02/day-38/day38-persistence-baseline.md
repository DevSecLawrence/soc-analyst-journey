# Day 38 — Persistence Baseline

This is the normal side of the picture.

## Registry Run Keys
- Normal: software updaters, chat apps, enterprise agents
- Suspicious: random names, user profile paths, encoded command lines

## Scheduled Tasks
- Normal: maintenance, update checks, backup jobs
- Suspicious: hidden tasks, odd trigger times, PowerShell or LOLBin payloads

## Services
- Normal: signed software, drivers, endpoint agents
- Suspicious: new service names that do not match the file path or vendor

## WMI Subscriptions
- Normal: rare in small environments
- Suspicious: almost anything here deserves a closer look

## Startup Folder
- Normal: user shortcuts for legit apps
- Suspicious: shortcuts that launch scripts, PowerShell, or dropped binaries