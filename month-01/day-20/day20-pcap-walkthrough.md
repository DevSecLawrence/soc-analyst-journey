# Day 20 — PCAP Walkthrough

Purpose: Reproducible, step-by-step notes for analyzing the PCAP and teaching a junior analyst how I reached conclusions.

## Environment & Tools
- Wireshark (version: fill)
- tshark
- Zeek (optional)
- Suricata / Bro logs (optional)

## Files
- Place PCAP(s) in `screenshots/` alongside annotated screenshots.

## Quick Commands
Example commands I use to triage a new PCAP:

```bash
# List top protocols
tshark -r sample.pcap -q -z io,phs

# Show HTTP requests
tshark -r sample.pcap -Y "http.request" -T fields -e frame.number -e ip.src -e http.host -e http.request.uri

# Export conversations
tshark -r sample.pcap -q -z conv,tcp

# Follow a TCP stream in Wireshark (GUI): right-click packet -> Follow -> TCP Stream
```

## Key Sessions I Checked (example)
- DNS: look for suspicious query patterns and NXDOMAIN spikes.
- HTTP: GET/POST to unknown hosts, long URIs, or obvious C2 patterns.
- TLS: certificate mismatches (CN vs host), unusual SNI.
- SMB/NetBIOS: internal lateral movement indicators.

## Packet Inspection Notes
- Follow the TCP stream for session 123 -> observed HTTP POST to `bad-domain.example` with EXE download.
- Extracted server IP `1.2.3.4` and TLS certificate CN `unrelated.example` (suspicious).

## Screenshots (place in `screenshots/`)
- pcap-overview.png — Wireshark Protocol Hierarchy
- follow-stream-123.png — Follow TCP Stream output
- extracted-http-headers.png — HTTP request/response headers

Insert annotated screenshots into the report files when available. Remove or redact any hostnames/IPs that contain internal or personal data before committing.
