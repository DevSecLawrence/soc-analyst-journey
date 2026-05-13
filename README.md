# SOC Analyst Journey (180-Day Execution)

This repo is a public SOC analyst portfolio built through daily hands-on labs. Each day includes evidence (artifacts) and reasoning (write-ups).

## What This Demonstrates
- Packet and protocol analysis (PCAP-based)
- Log interpretation and field extraction
- SIEM investigation thinking (Splunk/Elastic/KQL as the roadmap progresses)
- Detection engineering fundamentals (rules, queries, and false-positive reasoning)
- Clear analyst communication: conclusions, assumptions, uncertainties

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

## How To Review
Start with `month-01/day-01/`

Each day contains:
- A written analysis
- Supporting artifacts (PCAPs/logs/scripts) referenced in the write-up

## Safety / Scope
All activity is local and controlled. No external targeting.

Public artifacts are kept non-sensitive (e.g., controlled traffic generation; no logins/tokens in PCAPs).
Sensitive data is avoided in public artifacts.
