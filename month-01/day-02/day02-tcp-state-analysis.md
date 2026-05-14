# Day 2 — TCP Handshake State Analysis

## What I Concluded
- TCP has a very clear pattern when things are normal: SYN, SYN-ACK, ACK.
- When packets do not follow that pattern, it stands out pretty fast in Wireshark.
- The main thing I learned is that TCP makes a lot more sense when you think in states, not just flags and start observing more.

## Assumption I Made
- I thought a handshake was just a quick setup step, but it actually matters a lot when packets arrive out of order or never finish.

## Uncertainty I Have
- I still want to understand why some targets send RST and others just stay quiet when the handshake is wrong.

## Planned Evidence
- Full handshake capture to a local web server on port 80(http).
- A SYN with no follow-up.
- A SYN-ACK without a prior SYN.
- An ACK sent to a closed port.

## Notes
- In Wireshark, I need to watch SEQ, ACK, flags, and the state of the connection.
- Keep the target local or internal only.