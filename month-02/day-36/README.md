# Day 36 — PowerShell Logging and Analysis

Enabled all three PowerShell logging mechanisms on my Windows host using Group Policy — Script Block Logging (Event ID 4104), Module Logging (Event ID 4103), and Transcription. Verified each one was actually capturing data. Then documented 5 malicious PowerShell patterns from real threat reports and wrote a Sigma rule for each.

Main thing I learned: without logging enabled, you see that PowerShell ran. With it enabled, you see what it ran, decoded. That's the whole difference.

## Files
- [day36-powershell-logging.md](./day36-powershell-logging.md) — main write-up: what I did, what I concluded, what surprised me
- [day36-logging-config-guide.md](./day36-logging-config-guide.md) — step-by-step guide to enabling all three logging mechanisms
- [day36-malicious-powershell-patterns.md](./day36-malicious-powershell-patterns.md) — 5 attack patterns with obfuscation techniques and detection approaches
- [day36-powershell-sigma-rules/](./day36-powershell-sigma-rules/) — 5 Sigma detection rules
  - [encoded-command.yml](./day36-powershell-sigma-rules/encoded-command.yml)
  - [iex-download-cradle.yml](./day36-powershell-sigma-rules/iex-download-cradle.yml)
  - [amsi-bypass.yml](./day36-powershell-sigma-rules/amsi-bypass.yml)
  - [credential-harvesting.yml](./day36-powershell-sigma-rules/credential-harvesting.yml)
  - [lolbin-via-powershell.yml](./day36-powershell-sigma-rules/lolbin-via-powershell.yml)