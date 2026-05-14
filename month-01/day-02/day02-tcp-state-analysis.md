# Day 2 — TCP Handshake State Analysis

## What I Concluded
- A normal TCP handshake follows a predictable state change: SYN, SYN-ACK, ACK.
- Half-open or out-of-state packets create responses that help reveal scans or malformed traffic.
- TCP detection is easier when you understand the state machine, not just the flags.

## Assumption I Made
- I assumed a handshake was always “simple,” but TCP behavior changes when packets arrive out of order or without the expected follow-up.

## Uncertainty I Have
- I want to confirm why some targets reply with RST while others stay silent on invalid or incomplete handshakes.

## Planned Evidence
- Full handshake capture to a local web server on port 80.
- SYN with no follow-up.
- SYN-ACK without a prior SYN.
- ACK to a closed port.

## Notes
- Use Wireshark to annotate SEQ, ACK, flags, and connection state for each packet.
- Keep the target local or internal only.