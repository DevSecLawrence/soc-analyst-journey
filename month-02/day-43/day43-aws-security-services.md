# Day 43 — AWS Security Services Reference
 
**Date:** 2026-06-24
 
---
 
## Core Security Services
 
| Service | What it does | On-premise equivalent |
|---------|-------------|----------------------|
| IAM | Identity and access management — controls who can do what | Active Directory |
| CloudTrail | API audit logging — records every action taken in the account | Windows Security Event Logs |
| GuardDuty | Managed threat detection — analyses logs for suspicious behaviour | SIEM with detection rules |
| Security Hub | Consolidated security findings from all AWS services | SOC dashboard |
| S3 | Object storage — most commonly misconfigured service | File server |
| VPC Security Groups | Stateful firewall rules for resources | Windows Firewall / network ACL |
| AWS Config | Tracks configuration changes to AWS resources | Change management system |
 
---
 
## IAM Concepts
 
| Concept | What it is | Security relevance |
|---------|-----------|------------------|
| User | Long-term identity for humans or apps | Compromise = persistent access |
| Role | Temporary identity assumed by services | Least privilege for EC2/Lambda |
| Policy | JSON document defining permissions | Misconfiguration = privilege escalation |
| Access Key | Programmatic credentials | If leaked = full account compromise |
| MFA | Multi-factor authentication | Critical for all human users especially root |
 
**Least privilege principle:** Every IAM entity should have only the permissions required for its specific function. Nothing more.
 
**Root account rule:** The root account has unrestricted access to everything in the AWS account. It should only be used to create the first admin user and then locked away with MFA and no access keys generated.
 
---
