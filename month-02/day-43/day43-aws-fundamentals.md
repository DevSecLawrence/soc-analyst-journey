# Day 43 — Cloud Security Fundamentals: AWS
 
**Date:** 2026-06-24
**Resources used:** AWS documentation, AWS Free Tier account
**Focus:** Understanding how security works differently in the cloud
 
---
 
## The Mindset Shift
 
Before today I thought of security as something you do to servers and endpoints you physically control. Cloud security broke that assumption almost immediately.
 
In AWS, you don't own the hardware. You don't control the hypervisor. You can't install Sysmon on the underlying infrastructure. The security model is fundamentally different — and if you approach it with on-premise thinking you'll miss half the attack surface.
 
The concept that changed how I think about this: **Identity IS the perimeter.**
 
On-premise security is built around network perimeters — firewalls, VLANs, segment everything. Cloud security is built around identity — IAM roles, policies, and permissions are the actual boundary between what an attacker can and can't do. Compromising an IAM key is the cloud equivalent of getting domain admin. The network is almost irrelevant if the credentials are compromised.
 
---
 
## The Shared Responsibility Model
 
This is the foundational concept of cloud security and it's not obvious until someone explains it properly.
 
AWS secures **of** the cloud — the physical datacentres, the hardware, the hypervisor, the network infrastructure that connects everything. You can't touch any of that, and you don't need to worry about it.
 
You secure **in** the cloud — your data, your applications, your OS configurations (for EC2 instances), your IAM permissions, your network access controls, your logging configuration.
 
The practical implication: if you misconfigure an S3 bucket and make it publicly readable, that's your problem, not AWS's. AWS gave you the tool and secured the underlying infrastructure. You configured it wrong. This distinction is what makes cloud security breaches happen — not AWS failures, but customer misconfigurations.
 
---
## AWS Security Services Explored
 
### IAM (Identity and Access Management)
 
This is the most critical AWS security service. Everything in AWS is controlled through IAM.
 
**Users** — represent actual humans or applications that need to interact with AWS. Each user has credentials (password for console, access keys for API).
 
**Roles** — like users but designed to be assumed temporarily. An EC2 instance can assume a role to get permissions to access S3 without needing hardcoded credentials. This is the right way to grant permissions in AWS.
 
**Policies** — JSON documents that define what actions are allowed or denied on which resources. Attached to users, groups, or roles.
 
**Key security principle — least privilege:** Every user and role should have only the permissions they actually need and nothing more. An IAM user that only needs to read from one S3 bucket should not have permissions to create EC2 instances.
 
**What attackers do with IAM:**
- Steal access keys (exposed in GitHub repos, environment variables) → gain all permissions that key has
- Create new IAM users for persistence
- Escalate privileges by exploiting misconfigured policies
---

### CloudTrail
 
CloudTrail is the audit log for everything that happens in AWS. Every API call — creating a resource, deleting a resource, changing permissions, logging in — gets recorded.
 
**What it captures:**
- Who made the API call (which IAM user, role, or service)
- What action was taken (which API call)
- When it happened (timestamp with millisecond precision)
- Where it came from (source IP address)
- What the request parameters were
- Whether it succeeded or failed
**The log format is JSON.** Each event is a JSON object. An example entry looks like:
 
```json
{
  "eventTime": "2026-06-24T14:23:01Z",
  "eventName": "ConsoleLogin",
  "sourceIPAddress": "45.156.23.138",
  "userAgent": "Mozilla/5.0...",
  "userIdentity": {
    "type": "IAMUser",
    "userName": "labuser"
  },
  "responseElements": {
    "ConsoleLogin": "Success"
  }
}
```
 
**Security relevance:** CloudTrail is to AWS what Windows Security Event Logs are to Windows. Without it you're blind to what's happening in your account. With it you can reconstruct the full timeline of any incident.
 
**Default behaviour:** CloudTrail is NOT enabled by default on a new AWS account. You have to turn it on. This is a common misconfiguration — many organisations don't realise their AWS activity is going unlogged.
 
---
 ### GuardDuty
 
GuardDuty is AWS's managed threat detection service. It ingests CloudTrail logs, VPC Flow Logs, and DNS logs and applies threat intelligence and machine learning to identify suspicious activity.
 
**What it detects:**
- Unusual API calls (calling APIs not normally used in the account)
- Calls from known malicious IPs
- Credential exfiltration attempts
- Cryptocurrency mining (EC2 instances generating crypto = high compute bills)
- Unusual data access patterns in S3
**Key difference from CloudTrail:** CloudTrail records what happened. GuardDuty tells you what was suspicious. CloudTrail is the raw data. GuardDuty is the detection layer on top of it.
 
---
 
### S3 (Simple Storage Service) — Security Considerations
 
S3 buckets are the most commonly misconfigured AWS resource and one of the top causes of cloud data breaches. The configuration options that matter for security:
 
**Block Public Access** — a setting that prevents any bucket or object from being made publicly accessible. Should be enabled by default on every bucket that doesn't need public access.
 
**Bucket policies** — JSON documents defining who can access the bucket and what they can do. A misconfigured bucket policy that allows `"Principal": "*"` means the entire internet can access it.
 
**Access logging** — logs every request made to the bucket. Off by default. For security-sensitive buckets should always be on.
 
**The S3 breach pattern:** Developer creates a bucket, forgets to block public access, uploads sensitive data, data is indexed by a search engine or discovered by a threat actor scanning for open buckets. This has happened to major companies repeatedly.
 
---

