# Day 1 — OSI Model Analysis

## What I Concluded
- Layer 1 (Physical) failure: When the physical/link down, packets stop leaving the host.

- Layer 3(Routing) failure: I re routed my gateway to a fake gateway using ip route(del, add), i noticed when routing broken, ARP cannot resolve the next (default gateway).

- Layer 7 (Application) failure: I edited the host file (/etc/hosts) and added a test website and i noticed that at application-level name-to-destination mapping sends traffic to the wrong place.

## Assumption I Made
- I assumed “no internet” meant one problem, but it can happen at different OSI layers.

## Uncertainty I Have
- I want to confirm how DNS and the hosts file fit into Layer 7 versus lower layers.

