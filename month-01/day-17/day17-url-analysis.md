# Day 17 — URL Triage (PhishTank)

I pulled 5 verified phish URLs from PhishTank and started triaging them with URLScan and VirusTotal. Two are fully captured below, and the other three are noted as pending where I still need screenshots.

## Source
- PhishTank search (Valid = yes, Active = yes, Verified = yes)

## URL Triage Table

| Case | PhishTank ID | Original URL (defanged) | Target Brand | Final URL | Domain | IP | Hosting Country | VT Detections | URLScan Screenshot Result | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 |  | hxxps://jdidrogical-galileo.91-218-65-223.plesk[.]page/redirecte.php... | Unknown | (dead / 404) | jdidrogical-galileo.91-218-65-223.plesk.page | 91.218.65.223 | Frankfurt am Main, DE | 3/92 | 404 page | Suspicious (dead) |
| 2 |  | hxxps://invfort[.]one/id/login | Epic Games | https://www.epicgames.com/id/login/recovery/from-sign-in | www.epicgames.com | 104.18.21.94 | Ascension Island (Cloudflare) | 14/92 | Login page rendered | Suspicious (redirects to legit) |


## Case Notes

### Case 1
- Brand impersonated: Unknown (did not render a real page)
- Live or dead: Dead (404)
- Redirect chain: Not much to follow; it ends at a 404
- URLScan evidence: 404 screenshot and a simple one-hop request footprint
- VirusTotal signal: 3/92 vendors flagged it
- Verdict: Suspicious, but dead at the time of analysis

### Case 2
- Brand impersonated: Epic Games (based on final URL)
- Live or dead: Live (page rendered)
- Redirect chain: Submitted URL redirects to epicgames.com login recovery page
- URLScan evidence: Final URL is epicgames.com with a visible login page
- VirusTotal signal: 14/92 vendors flagged it
- Verdict: Suspicious source URL, but it ends on a legit domain


## Evidence
- Screenshots:
  - PhishTank results list (captured)
  - Case 1: VirusTotal + URLScan (captured)
  - Case 2: VirusTotal + URLScan (captured)

