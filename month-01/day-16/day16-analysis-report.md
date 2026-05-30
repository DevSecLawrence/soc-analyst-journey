# Day 16 — Phishing Ticket Write-Up (Header-Driven)

This is a training write-up, but I’m writing it like a real ticket: what happened, what the headers prove, and what I’d do next.

## Case Info
- Case ID: DAY16-S1-AUTO-PROTECTION
- Source: SpamAssassin public corpus (training sample)
- Priority: Low

---

## Executive Summary

- Subject: “Auto Protection”
- From says `netscape.net`, but Reply-To is `aol.com`.
- Received chain shows multiple relays before local delivery.
- No useful SPF/DKIM/DMARC here (old sample), so I’m leaning on header consistency + mismatches.
- Verdict: spam/suspicious (high confidence).

---

## What The User Saw

- Random “Auto Protection” email that they didn’t ask for.
- In a real mailbox: this is usually a click/reply trap.

---

## Header Findings (What I Can Prove)

### Sender Claims vs Reality
- Claimed From (From:): cristopherwotton@netscape.net
- Return-Path: <cristopherwotton@netscape.net>
- Reply-To: pmco811@aol.com
- Message-ID domain: N/A

### Authentication
- SPF result: not authenticated (MXToolbox showed SPF Authenticated failed)
- DKIM result: not authenticated
- DMARC result: not authenticated / not usable here
- Alignment notes: can’t talk alignment when SPF/DKIM aren’t passing

### Received Path
- Hop count: ~6+ hops
- First hop I wrote down (closest to origin): `Received: from netscape.net (mow-m20.webmail.aol.com [64.12.180.136]) by air-in01.mx.aol.com ...`
- Weird relays / suspicious hostnames:
	- netscape.net mail coming through AOL webmail infrastructure
	- multiple unrelated relays before local delivery (webnote.net, slashnull.org, etc.)
	- localhost/127.0.0.1 hops exist because of the corpus/fetchmail setup (noise, not attacker infrastructure)

---

## Indicators (Defanged)

| Type | Value | Notes |
|---|---|---|
| Sender | cristopherwotton@netscape.net | Claimed sender address |
| Reply-To | pmco811@aol.com | Mismatch vs From domain |
| Return-Path | cristopherwotton@netscape.net | Envelope sender domain |
| Domain | netscape.net | Visible From / Return-Path domain |
| Domain | aol.com | Reply-To domain |
| Domain | webnote.net | Seen in Received chain |
| Domain | slashnull.org | Seen in Received chain |
| Domain | jmason.org | Local delivery host in sample |
| URL | N/A | No URL extracted from the header snippet used |
| IP | 193[.]120[.]211[.]219 | webnote.net hop (from header) |
| IP | 64[.]12[.]136[.]5 | imo-m02.mx.aol.com hop (from header) |
| IP | 64[.]12[.]180[.]136 | mow-m20.webmail.aol.com hop (from header) |
| Hash | N/A | Not applicable for this header-only sample |

---

## Verdict + Confidence
- Verdict (Likely phishing / Likely legit / Suspicious): Suspicious / spam
- Confidence (Low/Med/High): High (spam corpus + Reply-To mismatch + no auth)

---

## Recommended Actions
- Containment:
	- Quarantine/remove the message from any real inbox
	- Search for similar subject/sender/Reply-To across mail logs
- Eradication:
	- If it’s repeated: block patterns (Reply-To domain, sender strings)
- User guidance:
	- Don’t click, don’t reply
	- Report similar emails immediately
- Preventative controls:
	- Tight inbound filtering + link protections
	- DMARC enforcement for *your* domains (baseline requirement)

---

## Evidence
- Screenshots:
	- s1-raw-header.png
	- s1-mxtoolbox-summary.png

![S1 raw header snippet](./screenshots/s1-raw-header.png)

![S1 MXToolbox summary](./screenshots/s1-mxtoolbox-summary.png)
