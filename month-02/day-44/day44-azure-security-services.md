# Day 44 — Azure Security Services Reference
 
**Date:** 2026-06-25
 
---
 
## Core Security Services
 
| Service | What it does | AWS Equivalent |
|---------|-------------|---------------|
| Entra ID (Azure AD) | Cloud identity — users, groups, roles, conditional access | IAM (but broader scope) |
| Activity Log | Control plane audit log — who did what to which resource | CloudTrail |
| Defender for Cloud | Security posture + threat detection | GuardDuty + Security Hub combined |
| Microsoft Sentinel | Cloud-native SIEM — detection, investigation, response | Security Hub (but much more capable) |
| Network Security Groups | Stateful firewall rules for resources | Security Groups |
| Azure Monitor | Infrastructure and application monitoring | CloudWatch |
| Key Vault | Secret and certificate management | AWS Secrets Manager |
| Azure Policy | Enforce compliance rules across resources | AWS Config Rules |
 
---
 
## Entra ID Concepts
 
| Concept | What it is | Security relevance |
|---------|-----------|------------------|
| User | Human or app identity | Compromise = access to all Microsoft services |
| Group | Collection of users for easier management | Overprivileged group = lateral movement risk |
| Role | Set of permissions assigned to a scope | Global Administrator = highest risk role |
| Service Principal | App identity (Azure equivalent of IAM role for apps) | Exposed credentials = app-level compromise |
| Managed Identity | Auto-managed identity for Azure resources | Preferred over service principals with static keys |
| Conditional Access | Policy-based access control | Block access from non-compliant devices |
| Privileged Identity Management | Just-in-time privileged access | Reduces standing privilege exposure |
 
---

## Activity Log Fields — Security Relevant
 
| Field | What it contains | Why it matters |
|-------|----------------|---------------|
| `operationName` | What action was taken | What happened |
| `caller` | Who made the call | Attribution |
| `eventTimestamp` | When it happened | Timeline |
| `callerIpAddress` | Source IP | Geolocation, anomaly detection |
| `status` | Success or failure | Failed operations = reconnaissance |
| `resourceId` | Which resource was affected | Scope of action |
| `properties` | Additional context | Specific details of the operation |
 
---

## Common Azure Misconfiguration Patterns
 
| Misconfiguration | What it enables | Detection signal |
|-----------------|----------------|-----------------|
| Global Administrator overuse | Single account controls everything | Any GA login from unusual IP |
| Guest users with high privileges | External account has broad access | Guest + Owner/Contributor role assignment |
| No Conditional Access policies | MFA bypass possible | Successful login from risky location |
| Storage blob public access enabled | Data exposed to internet | Storage account public access setting change |
| NSG allowing 0.0.0.0/0 on RDP | Internet-facing RDP | NSG rule allowing port 3389 from any |
| Diagnostic settings not configured | No audit trail | Activity Log retention gap |
| No MFA on privileged accounts | Password alone = full access | Sign-in risk events without MFA |
