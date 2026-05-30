# Day 16 — My Email Header Checklist (Phishing Triage)

If a “is this phishing?” ticket hits my queue, this is what I check.

## 1) Quick Identity Checks
- [ ] Compare `From` vs `Reply-To`
- [ ] Check `Return-Path` domain (does it match `From`?)
- [ ] Check `Message-ID` domain (does it match the org sending it?)

## 2) Authentication (Don’t Misread It)
- [ ] SPF result (pass/fail/softfail/neutral)
- [ ] DKIM result (pass/fail)
- [ ] DMARC result (pass/fail)
- [ ] Alignment: does DKIM `d=` or SPF domain align with visible `From` domain?
- [ ] If SPF passes but alignment fails: check if Return-Path is a known vendor (Marketo/HubSpot/SES etc.) and see if DKIM alignment is what made DMARC pass

## 3) Received Chain
- [ ] Count hops
- [ ] Identify the first hop (closest to the origin)
- [ ] Look for weird hostnames / mismatched HELO names / strange relays

## 4) Red Flags That Matter
- [ ] Reply-To mismatch + urgency language
- [ ] New/unfamiliar sending infrastructure for a known brand
- [ ] Auth pass but still suspicious (compromised vendor mail, abused legit service)
- [ ] SPF alignment fail by itself is not “gotcha” — vendor sending does this all the time

## 5) What I Record (Minimum)
- [ ] From / Reply-To / Return-Path
- [ ] SPF/DKIM/DMARC results + alignment note
- [ ] Origin IP/domain (if visible)
- [ ] Verdict + confidence
- [ ] Recommended action
