# Day 39 — Credential Access and Protection

Credentials are what turn a small foothold into full domain compromise. Today I went through 5 techniques attackers use to steal them — LSASS dumping, SAM extraction, Credential Manager access, Kerberoasting, and browser credential theft. Documented how each works, what catches it, and what stops it. 5 detection rules written.

Windows VM still down — research and detection writing only. Hands-on pending lab rebuild.

## Files
- [day39-credential-access.md](./day39-credential-access.md) — analysis, conclusions, assumptions, uncertainties
- [day39-credential-techniques.md](./day39-credential-techniques.md) — 5 techniques broken down in detail
- [day39-credential-detections.md](./day39-credential-detections.md) — 5 Sigma detection rules
