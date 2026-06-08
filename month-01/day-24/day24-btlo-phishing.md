# Day 24 — Blue Team Labs Online: Phishing Email Investigation
 
**Date:** 2026-06-08
**Platform:** Blue Team Labs Online (free tier)
**Challenge:** Phishing Analysis
**Difficulty:** Easy
**Points:** 10/10
**Completed:** ✅

---

## Scenario
 
A user received a phishing email and forwarded it to the SOC. Investigate the email and attachment to collect useful artifacts.
 
---
 
## Initial Hypothesis
 
Before opening the file — the scenario says "phishing email forwarded to SOC." My assumption was this would be a credential harvesting attempt, probably impersonating a well known brand, with a link to a fake login page. Classic phishing playbook.
 
That turned out to be partially right but with a twist — it wasn't a direct link to a fake login. It had a nested attachment with the malicious URL buried inside it.
 
---

## Investigation
 
### Tools Used
- VS Code — to read the raw `.eml` file
- `whois.domaintools.com` — for reverse DNS
- `url2png.com` — to safely preview the malicious URL without visiting it
- `base64decode.org` — to decode the base64 email body
### Step 1 — Read the email headers in VS Code
 
Opened the `.eml` file in VS Code and searched through the raw headers.
 
**Primary recipient:** `kinnar1975@yahoo.co.uk`
 
**Subject:** `Undeliverable: Website contact form submission`
 
First red flag right there — the subject is a delivery failure notice. That's a social engineering technique. The target thinks a legitimate email bounced and opens the attachment to investigate. The attachment is the payload.
 
**Sending IP:** Found in the `Received:` headers
**Resolved host (reverse DNS):** `c5s2-1e-syd.hosting-services.net.au`
 
Ran the IP through `whois.domaintools.com` to get the resolved hostname. A `.net.au` hosting provider sending a delivery failure notice for what looks like a web form submission — that's suspicious.
 
### Step 2 — Open the attachment
 
The attached file was: `Website contact form submission.eml`
 
A `.eml` file inside a `.eml` file — the phishing email contained another email as its attachment. That nested email had the malicious URL inside it.
 
**Malicious URL found inside the attachment:**
`https://35000usdperwwekpodf.blogspot.sg?p=3D9swghttps://35000usdperwwekpodf.blogspot.sg`
 
The domain name alone (`35000usdperwwekpodf`) is a massive red flag — no legitimate service uses a domain like that.

