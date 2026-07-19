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
## Which One Will I See in a SOC Role?
 
**Entry level SOC in a large Nigerian enterprise or multinational:** More likely Azure — enterprises running Windows and Office 365 almost always extend to Azure
 
**Tech companies and startups:** More likely AWS
 
**Government and public sector:** Varies — increasingly cloud but often Microsoft-heavy
 
**Remote roles for UK/EU/US companies:** Both, depending on the company. Many use both simultaneously
 
**The practical advice:** Learn both conceptually. Go deeper on whichever platform appears in job descriptions you're targeting. The concepts transfer — the terminology doesn't.
 
---
 
## What Transfers Between Both Clouds
 
If you understand security in one cloud, you're 70% of the way to understanding the other. The principles are identical:
 
- Identity is the primary attack surface
- Misconfiguration is the most common vulnerability
- Logging is the foundation of detection
- Shared responsibility defines what you're responsible for
- Least privilege applies to all permissions
What doesn't transfer: specific service names, log field names, console interfaces, and some capability nuances. Those you just have to look up.

