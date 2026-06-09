# Executive Summary — Phishing Incident
 
**Date:** 2026-06-08
**Prepared by:** Lawrence (SOC Analyst)
**For:** CISO
**Risk Level:** Medium
**Status:** Closed
 
---
 
A user in our organisation received a phishing email designed to look like a failed delivery notification. The email had a malicious link hidden inside an attachment — specifically buried inside a second email file attached to the first, which is an evasion technique designed to bypass automated scanning tools. The link pointed to a page hosted on Google's Blogspot platform, which attackers use deliberately because Google's reputation means it often gets past URL filters. The malicious page has been taken down and we have no evidence the user clicked the link or had their credentials compromised, but we cannot fully confirm this without interviewing them directly. Recommended actions are to block the malicious domain, update our email scanning configuration to inspect nested attachments, and contact the affected user to confirm they didn't interact with the content before forwarding it to us.
 