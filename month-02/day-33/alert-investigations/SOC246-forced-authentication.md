# Alert Investigation — SOC246: Forced Authentication Detected
 
**Date:** 2026-06-24
**Platform:** LetsDefend
**Event ID:** 208
**Alert:** SOC246 - Forced Authentication Detected
**Severity:** Medium
**Category:** Web Attack
**Event Time:** Dec 12, 2023, 02:15 PM
 
---
 
## Alert Details
 
| Field | Value |
|-------|-------|
| Rule | SOC246 - Forced Authentication Detected |
| Level | Security Analyst |
| Source IP | 120.48.36.175 |
| Destination IP | 104.26.15.61 |
| Host | WebServer_Test |
| Request URL | http://test-frontend.letsdefend.io/accounts/login |
| Request Method | POST |
| Device Action | Permitted |
| Alert Trigger Reason | Multiple POST requests seen from the same IP to the fixed URI "/accounts/login" |
 
---

## My Initial Hypothesis
 
Before digging in: multiple POST requests from the same IP to a login endpoint is almost textbook credential stuffing or brute force. The attacker is trying to authenticate by hammering the login page with different username/password combinations. The fact that the device action was "Permitted" means the traffic wasn't blocked — which means either the requests looked legitimate enough to pass through, or there's no rate limiting on the login endpoint.
 
---
 
## Investigation
 
**Step 1 — Read the alert trigger reason**
 
"Multiple POST requests were soon seen from the same IP to the fixed URI /accounts/login."
 
That's the pattern. One IP, many requests, same endpoint. This is forced authentication — repeatedly attempting to authenticate using automated tools. The attacker is likely cycling through credential lists hoping one combination works.
 
**Step 2 — Check the source IP**
 
Source IP: `120.48.36.175`
 
This is an external IP hitting the login page of a web server. The destination `104.26.15.61` is the web server's IP. The request method is POST — that's correct for a login form submission.
 
I'd want to run this IP through threat intelligence tools:
- VirusTotal: check if it's flagged as malicious
- AbuseIPDB: check if it's been reported for brute force activity before
- Shodan: see what else is running on this IP
**Step 3 — Assess the device action**
 
Device action: **Permitted**
 
This is the critical detail. The traffic wasn't blocked. That means either:
- The firewall/WAF has no rate limiting rule for login endpoints
- The requests were spread out enough to avoid triggering rate limits
- There is no automated blocking in place
A "Permitted" status on a brute force alert means the attack was ongoing and potentially still running when this alert fired. This isn't a historical event — it's active.

**Step 4 — Determine true positive or false positive**
 
Is this a real attack or a misconfiguration / pen test?
 
Arguments for true positive:
- External IP hitting a login endpoint repeatedly
- POST method to /accounts/login specifically — not random crawling
- Alert trigger reason explicitly says "multiple POST requests from the same IP"
- Traffic was permitted — no internal blocking suggests this wasn't an authorised test
I'd classify this as a **True Positive** pending further investigation.
 
**Step 5 — What I'd do next**
 
1. Block the source IP `120.48.36.175` at the firewall level immediately
2. Check authentication logs for the login endpoint — did any of the attempts succeed? If yes, which account and when?
3. If any attempt succeeded — lock that account, force password reset, investigate what the account accessed after login
4. Check for other IPs hitting the same endpoint in the same timeframe — brute force campaigns often use multiple IPs simultaneously
5. Recommend rate limiting and account lockout policies to the web server team if they're not already in place
6. Check if this IP has hit any other endpoints on the server — lateral recon after finding an open login page is common
---

