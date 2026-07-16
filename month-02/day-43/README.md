# Day 43 — Cloud Security Fundamentals: AWS

Cloud security is not optional anymore. Today was about understanding how security works differently when you don't own the hardware. Explored IAM, CloudTrail, GuardDuty, S3, and VPC security groups. The shared responsibility model is the concept everything else builds on.

Key shift: in on-premise security the perimeter is the network. In cloud security the perimeter is identity. Compromising an IAM key is the cloud equivalent of getting domain admin.

## Files
- [day43-aws-fundamentals.md](./day43-aws-fundamentals.md) — how AWS security works, shared responsibility model, conclusions
- [day43-aws-security-services.md](./day43-aws-security-services.md) — service reference, IAM concepts, misconfiguration patterns
- [day43-cloudtrail-analysis.md](./day43-cloudtrail-analysis.md) — CloudTrail log format, sample events, 3 detection concepts
- [screenshots](./screenshots/)