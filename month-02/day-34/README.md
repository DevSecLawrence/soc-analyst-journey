# Day 34 — Sysmon Deep Dive: The Free EDR Telemetry Source

Windows VM still down so no live testing. Went back into the LetsDefend Sysmon logs to study specific Event IDs properly, read through SwiftOnSecurity and Olaf Hartong's configs on GitHub, then wrote a custom config from scratch. Config is untested pending lab rebuild.

Main thing I learned: installing Sysmon without configuring it is like buying a CCTV system and pointing all the cameras at the ceiling.

## Files
- [day34-sysmon-deep-dive.md](./day34-sysmon-deep-dive.md) — main write-up, what Sysmon is, what I concluded
- [day34-event-id-reference.md](./day34-event-id-reference.md) — personal reference for the Event IDs that matter most
- [day34-custom-sysmon-config.xml](./day34-custom-sysmon-config.xml) — custom config: PowerShell execution, non-standard network connections, Temp directory drops, registry persistence (⚠️ untested)