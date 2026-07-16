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
## CloudTrail Log Fields — Security Relevant
 
| Field | What it contains | Why it matters |
|-------|----------------|---------------|
| `eventTime` | When the API call happened | Timeline reconstruction |
| `eventName` | Which API was called | What action was taken |
| `userIdentity` | Who made the call | Attribution |
| `sourceIPAddress` | Where the call came from | Geolocation, anomaly detection |
| `errorCode` | If the call failed, why | Failed actions = reconnaissance |
| `requestParameters` | What parameters were passed | What was being done to what resource |
| `responseElements` | What the API returned | Whether the action succeeded |
 
---
## Common Misconfiguration Patterns
 
| Misconfiguration | What it enables | How to detect |
|-----------------|----------------|--------------|
| S3 bucket public access | Data exposed to internet | S3 Block Public Access disabled, ACL set to public |
| Security group 0.0.0.0/0 on port 22 | SSH brute force from internet | VPC Flow Logs + Security Group changes |
| Root account used regularly | High-impact credentials in use daily | CloudTrail: ConsoleLogin with Root identity |
| Access keys in GitHub repos | Stolen credentials, account compromise | GitHub secret scanning, CloudTrail unusual IP |
| MFA not enabled on IAM users | Credential stuffing succeeds | IAM credential report |
| CloudTrail disabled | No audit trail for incident response | CloudTrail: StopLogging event |
 
---
