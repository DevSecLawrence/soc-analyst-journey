# Day 44 — Cloud Security Fundamentals: Azure

Day 43 was AWS. Day 44 is Azure. Most enterprises use both and Microsoft-heavy environments lean Azure heavily. The concepts map across — IAM becomes Entra ID, CloudTrail becomes Activity Log, GuardDuty becomes Defender for Cloud. The terminology changes but the analyst thinking doesn't.

Biggest finding: Microsoft Sentinel is a real SIEM that uses KQL natively — the same query language from Sigma rule conversion. That's directly applicable.

## Files
- [day44-azure-fundamentals.md](./day44-azure-fundamentals.md) — Azure security concepts, services, 3 detection concepts, conclusions
- [day44-azure-security-services.md](./day44-azure-security-services.md) — service reference, Entra ID concepts, misconfiguration patterns
- [day44-aws-vs-azure.md](./day44-aws-vs-azure.md) — side by side comparison, log format differences, which cloud you'll see in SOC roles
-[screenshots](./screenshots/)