# Day 37 — Living Off the Land: LOLBAS Techniques

Attackers use tools that are already on Windows so their malware looks legitimate. Today I went through 10 LOLBAS binaries from lolbas-project.github.io — what each one does legitimately, how attackers abuse it, and what the command line looks like when it's being used maliciously. Wrote 5 Sigma detection rules targeting the abuse patterns.

The hard part isn't identifying the binaries. It's writing detections that catch the malicious use without firing on the legitimate use. Context is everything.

## Files
- [day37-lolbas.md](./day37-lolbas.md) — what I concluded, assumption I made, uncertainty I have
- [day37-lolbas-reference.md](./day37-lolbas-reference.md) — 10 binaries documented with abuse techniques and process trees
- [day37-lolbas-detections/](./day37-lolbas-detections/) — 5 Sigma rules
  - [certutil-download.yml](./day37-lolbas-detections/certutil-download.yml)
  - [mshta-execution.yml](./day37-lolbas-detections/mshta-execution.yml)
  - [regsvr32-squiblydoo.yml](./day37-lolbas-detections/regsvr32-squiblydoo.yml)
  - [wmic-process-creation.yml](./day37-lolbas-detections/wmic-process-creation.yml)
  - [msiexec-remote.yml](./day37-lolbas-detections/msiexec-remote.yml)