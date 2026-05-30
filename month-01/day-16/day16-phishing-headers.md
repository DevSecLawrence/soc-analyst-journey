# Day 16 — Phishing Analysis: Header Dissection

## What Today Is About
Phishing triage starts here. The body can lie. The From address can lie. The header chain is where you figure out what *actually happened*.

---

## Sample Set (Track What You Analyzed)

Fill this in as you go.

| Sample ID | Type (Legit / Suspicious) | Source (Your inbox / SpamAssassin) | Subject | Claimed From | Return-Path domain | Reply-To domain | Your verdict |
|---|---|---|---|---|---|---|---|
| L1 | Legit | Your inbox | NetAcad Student Newsletter  April 2026 | Cisco Networking Academy <netacademail@external.cisco.com> |  <059-VFZ-834.0.1100893.0.0.34454.9.416187631@em-sj-77.mktomail.com> | netacademail@external.cisco.com |  |
| L2 | Legit | Your inbox | [Newsletter]  Netlify is now full-stack | Netlify Team <noreply@netlify.com> | 	<1axb9lvdcpn34bfn6j4jfeyp2rsoz4m51ae55n@bf53x.hubspotemail.net> | noreply@netlify.com |  |
| L3 | Legit | Your inbox |  Thanks for joining NEWBIE HIKE WITH IKEM MAZELI | The Hikerstrail Trybe <hikerstrail@calendar.luma-mail.com> | <0101019e547e8683-5908b236-a1ad-438b-80b3-3f8ae323eafe-000000@amazonses.calendar.luma-mail.com> | The Hikerstrail Trybe <thehikerstrailng@gmail.com> |  |
| S1 | Suspicious | SpamAssassin | Auto Protection |cristopherwotton@netscape.net  | <cristopherwotton@netscape.net> |     pmco811@aol.com |  |
| S2 | Suspicious | SpamAssassin |  [ILUG] Prevent Work Monotony ilug | Paula Gaiger <Rocheldy@webinfo.fi> | 	<ilug-admin@linux.ie> | 	<ilug@skynet.csn.ul.ie> |  |
| S3 | Suspicious | SpamAssassin | Webmaster ganhe dinheiro !!! | "PARQUIEJO DII TROYA" <webmaster@ibest.com.br> | <webmaster@ibest.com.br> | diitroya@ibest.com.br |  |

---

## Header Breakdown (One Section Per Sample)

### Sample L1

**Copy/paste the auth summary** (SPF/DKIM/DMARC lines from the header or Gmail “Show original”).

**Key fields (paste exact values):**
- From:
- Reply-To:
- Return-Path:
- Message-ID:

**Received chain (trace the path):**
Paste the `Received:` lines in order (top to bottom). Then answer:
- How many hops?
- Does the first hop look like the real sender or a relay?

**Auth results (record exactly):**
- SPF:
- DKIM:
- DMARC:

**Red flags I saw (if any):**
- 

**My call (why I think it’s legit):**
- 

---

### Sample L2

(Repeat the same template)

---

### Sample L3

(Repeat the same template)

---

### Sample S1

(Repeat the same template)

---

### Sample S2

(Repeat the same template)

---

### Sample S3

(Repeat the same template)

---

## What I Concluded

## Assumption I Made

## Uncertainty I Have
