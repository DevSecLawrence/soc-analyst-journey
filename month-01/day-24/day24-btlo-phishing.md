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

### Step 3 — Identify the hosting service
 
The malicious URL is on `blogspot.sg` — that's **Blogspot**, Google's free blogging platform. Attackers abuse free hosting services because:
- They're free and easy to set up
- They use trusted domains that bypass basic URL filters
- They get taken down eventually but the attacker has already collected credentials by then
**Hosting service:** Blogspot
 
### Step 4 — URL2PNG
 
Pasted the URL into `url2png.com` to safely preview the page without visiting it.
 
**Heading text on the page:** `Blog has been removed`
 
The page was already taken down by the time I investigated — but the URL2PNG cache still had the heading confirming it existed. This is a standard finding in phishing investigations — by the time a user reports it and the SOC investigates, the page is often already down.
 
---

## Findings Summary
 
| Artifact | Value |
|---------|-------|
| Recipient | `kinnar1975@yahoo.co.uk` |
| Subject | `Undeliverable: Website contact form submission` |
| Sending IP resolved host | `c5s2-1e-syd.hosting-services.net.au` |
| Attached file | `Website contact form submission.eml` |
| Malicious URL | `https://35000usdperwwekpodf.blogspot.sg?p=3D9swg` |
| Hosting service | Blogspot |
| Page heading (via URL2PNG) | `Blog has been removed` |
 
---

## What I Concluded
 
This was a delivery failure lure — the attacker disguised the phishing email as a bounce notification to get the target to open the attachment. The attachment contained a second `.eml` file with the malicious Blogspot link inside it. The double-layer approach (email inside email) adds one more step between the target and the malicious URL, which can bypass some automated email scanners that only check the top-level email.
 
The attacker used Blogspot specifically because it's a Google-owned domain. A lot of email security tools whitelist Google domains by default. That's the whole point — the malicious content lives on a trusted infrastructure.
 
---
 
## Assumption I Made
 
I assumed the malicious URL would be in the main email body. It wasn't — it was inside a nested `.eml` attachment. That extra layer is deliberate. It adds friction for automated scanners and for analysts who don't dig into attachments carefully. I need to remember to always check attachments thoroughly, not just the email body.
 
---
 
## Uncertainty I Have
 
The reverse DNS came back as an Australian hosting provider. I don't know if that's where the attacker actually is or if they just rented a server there. IP geolocation and reverse DNS tell you where the infrastructure is, not where the attacker is. Those are two very different things and I need to be careful not to conflate them in a real investigation.
 
---

## Hypothesis Evolution
 
Started thinking: credential harvesting → fake login page → link in email body.
 
Actual attack: delivery failure lure → nested .eml attachment → Blogspot page → unknown payload (page already taken down).
 
The lure technique was more sophisticated than I expected for an "Easy" challenge. The nested attachment approach is something I hadn't seen before and it makes sense as an evasion technique once you understand it.
 