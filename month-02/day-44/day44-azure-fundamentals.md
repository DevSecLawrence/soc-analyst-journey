# Day 44 — Cloud Security Fundamentals: Azure
 
**Date:** 2026-06-25
**Resources used:** Azure documentation, Microsoft Learn, Azure Free Account
**Focus:** How Azure security compares to AWS after yesterday's deep dive
 
---
 
## Why Azure After AWS
 
Most enterprises don't use just one cloud. AWS dominates overall market share but Microsoft Azure dominates enterprise environments specifically — and for a reason that's easy to understand. Enterprises already run on Microsoft. Windows servers, Active Directory, Office 365, Exchange. Azure is the natural extension of that existing infrastructure into the cloud. An organisation that's already paying Microsoft for everything is more likely to add Azure than to add AWS.
 
As a SOC analyst, this means knowing AWS alone isn't enough. Most large enterprises use both, and the Microsoft-heavy ones lean Azure. Understanding both makes you genuinely useful across more environments.
 
---

## Azure vs AWS — The Mental Model
 
Before getting into specifics, the biggest conceptual difference: Azure is Microsoft's product, built for organisations that already use Microsoft. AWS was built for developers and startups first, enterprises second. That difference shows up in how everything is structured.
 
AWS thinks in terms of standalone services. Azure thinks in terms of suites — Azure Active Directory (now Entra ID) integrates with Office 365 integrates with Intune integrates with Defender. If you already use Microsoft products, Azure security feels native. If you don't, it feels complex.
 
---
 
## Azure Security Services

### Azure Entra ID (formerly Azure Active Directory)
 
This is the Azure equivalent of AWS IAM — but it's also more than that. Entra ID is Microsoft's cloud identity platform and it does things AWS IAM doesn't.
 
**Users and Groups** — same concept as AWS IAM users and groups. Users authenticate to Azure resources. Groups organise users for easier permission management.
 
**Roles** — Azure has built-in roles (Owner, Contributor, Reader) and custom roles. Assigned at different scopes: subscription level, resource group level, or individual resource level.
 
**Conditional Access** — this doesn't exist in AWS. Conditional Access lets you say "only allow login if the user is on a compliant device" or "require MFA if the login comes from outside the corporate network." It's policy-based access control on top of basic authentication.
 
**The key difference from AWS IAM:** Entra ID also handles authentication for Office 365, Teams, SharePoint, and every other Microsoft service. A compromised Entra ID account doesn't just give access to Azure resources — it potentially gives access to the entire Microsoft ecosystem. The blast radius of an Entra ID compromise is much larger.
 
**What attackers do with Entra ID:**
- Password spray attacks against Office 365 logins (which use Entra ID)
- Token theft — stealing authentication tokens to bypass MFA
- Creating guest accounts for persistence
- Privilege escalation via role assignment
---
 
### Azure Activity Log
 
The Azure equivalent of AWS CloudTrail. Records every operation performed on Azure resources — who did what, when, from where.
 
**What it captures:**
- Control plane operations (creating, modifying, deleting resources)
- Who performed the action (which user, service principal, or managed identity)
- When it happened
- Whether it succeeded or failed
- The source IP address
**What it doesn't capture by default:**
- Data plane operations (what's inside a storage blob, what queries ran against a database)
- Guest OS level activity (you need Azure Monitor for that)
**Log format:** JSON, similar to CloudTrail but different field names and structure.
 
**Key difference from CloudTrail:** Activity Log is enabled by default and retained for 90 days. CloudTrail is NOT enabled by default. Azure gets credit here — you have at least 90 days of control plane audit history even on a new account.
 
---
 
### Microsoft Defender for Cloud
 
Azure's version of AWS GuardDuty, but broader. Defender for Cloud provides:
 
**Security posture management** — continuously assesses your Azure resources against security best practices and gives you a Secure Score. A lower score means more misconfigurations.
 
**Threat protection** — detects active threats across Azure services, similar to GuardDuty's detection capability.
 
**Regulatory compliance** — maps your configuration to compliance frameworks (PCI DSS, ISO 27001, NIST).
 
**Key difference from GuardDuty:** GuardDuty is purely threat detection. Defender for Cloud combines threat detection with posture management — it tells you both "you're being attacked" and "you're configured in a way that makes attacks easier."
 
---

### Microsoft Sentinel
 
This is Azure's native SIEM — and it's a proper SIEM, not just a log aggregation service. Sentinel:
 
- Ingests logs from Azure Activity Log, Entra ID, Defender, and non-Microsoft sources
- Has built-in detection rules (similar to Sigma rules)
- Has a query language (KQL — which you've already written in for Sigma rule conversion)
- Has playbooks for automated response (equivalent of SOAR capabilities)
**Key difference from AWS Security Hub:** Security Hub is primarily a findings aggregation dashboard. Sentinel is a full SIEM with detection, investigation, and response capabilities. They're not equivalent — Sentinel is significantly more powerful for a SOC analyst.
 
**The KQL connection:** Everything in Sentinel is queried with KQL. If you've written Sigma rules converted to KQL, you can already write Sentinel queries. That's a real job skill that directly applies.
 
---
 
### Network Security Groups (NSGs)
 
Azure's equivalent of AWS Security Groups. Stateful firewall rules controlling inbound and outbound traffic to Azure resources.
 
Same concept, different interface. Rules are defined by source/destination IP, port, and protocol. Allow or deny.
 
**Key difference:** Azure NSGs can be applied at both the subnet level and the individual NIC level simultaneously. AWS Security Groups apply at the instance/ENI level. The layering in Azure gives more granular control but also more complexity.
 
---

