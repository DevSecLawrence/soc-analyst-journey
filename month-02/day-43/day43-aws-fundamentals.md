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


