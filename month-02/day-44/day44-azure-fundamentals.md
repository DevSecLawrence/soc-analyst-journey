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