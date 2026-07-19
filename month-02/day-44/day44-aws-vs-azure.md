# Day 44 — AWS vs Azure: Security Comparison
 
**Date:** 2026-06-25
 
---
 
## Side by Side
 
| Security Area | AWS | Azure | Key Difference |
|--------------|-----|-------|---------------|
| Identity | IAM | Entra ID | Entra ID covers Office 365 too — bigger blast radius on compromise |
| Audit logging | CloudTrail | Activity Log | Activity Log on by default (90 days). CloudTrail must be manually enabled |
| Threat detection | GuardDuty | Defender for Cloud | Defender combines posture + detection. GuardDuty is detection only |
| SIEM | Security Hub | Microsoft Sentinel | Sentinel is a full SIEM. Security Hub is more of a findings dashboard |
| Network firewall | Security Groups | Network Security Groups | Both stateful. Azure NSGs apply at subnet AND NIC level |
| Secret management | Secrets Manager | Key Vault | Near-equivalent |
| Compliance monitoring | AWS Config | Azure Policy + Defender | Azure tooling more tightly integrated |
| Query language | N/A (SPL for Splunk integration) | KQL (Sentinel native) | KQL is directly usable from Sigma rule conversion work |
 
---

## Log Format Comparison
 
### CloudTrail (AWS)
```json
{
  "eventTime": "2026-06-24T14:23:01Z",
  "eventName": "CreateUser",
  "userIdentity": {
    "type": "IAMUser",
    "userName": "admin"
  },
  "sourceIPAddress": "197.210.65.42",
  "requestParameters": {
    "userName": "testuser"
  }
}
```
 
### Activity Log (Azure)
```json
{
  "eventTimestamp": "2026-06-25T09:14:22Z",
  "operationName": "Microsoft.Authorization/roleAssignments/write",
  "caller": "admin@tenant.onmicrosoft.com",
  "callerIpAddress": "197.210.65.42",
  "status": "Succeeded",
  "resourceId": "/subscriptions/xxx/resourceGroups/rg-day44",
  "properties": {
    "roleDefinitionId": "Owner",
    "principalId": "user-object-id"
  }
}
```
 
**Key differences:**
- AWS uses `eventName`, Azure uses `operationName`
- AWS uses `userIdentity.userName`, Azure uses `caller`
- AWS uses `sourceIPAddress`, Azure uses `callerIpAddress`
- Azure `operationName` uses a resource provider format (`Microsoft.X/Y/action`) — more verbose but more descriptive
---
 
# Shared Responsibility — Both Clouds
 
The shared responsibility model is identical in both:
 
**Cloud provider secures:** Physical datacentres, hardware, hypervisor, network infrastructure, managed service platforms
 
**Customer secures:** Identity configuration, data, application security, OS patches (for IaaS), network access controls, logging configuration
 
The line is in the same place. The tools to manage your side of it are just different.
 
---
