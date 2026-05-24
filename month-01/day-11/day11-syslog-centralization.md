# Day 11 — Syslog Standard and Log Centralization

## What I Concluded

Today was less about terminal work and more about 
understanding the infrastructure that makes a SOC 
actually function.

The medium exercise was straightforward — install 
rsyslog, generate messages at all 8 severity levels 
using the logger command, and find them in syslog. 
What I didn't expect was that all 8 showed up including 
severity 7 (debug). A lot of rsyslog configs filter 
debug out by default to save storage. Mine didn't. 
That's something to note — in a production environment 
you'd want to make that decision deliberately, not 
accidentally.

The syslog format my messages came out in:
2026-05-24T18:07:58.737276+01:00 kali lawrence:
DAY11-TEST: severity 0 - emergency

Breaking that down:
- **2026-05-24T18:07:58** — ISO 8601 timestamp
- **+01:00** — timezone offset included (WAT)
- **kali** — hostname
- **lawrence** — process/user that sent it
- **DAY11-TEST: severity 0 - emergency** — message body

This is actually cleaner than the syslog format I saw 
on Day 8. rsyslog on newer systems uses RFC 5424 format 
which includes timezone — the old BSD syslog format 
from Day 8 didn't. Same protocol name, two different 
format versions, and the difference matters for 
correlation.

The PRI value is what ties facility and severity 
together. The formula:
PRI = (Facility × 8) + Severity

For my user.info message:
- user facility = 1
- info severity = 6
- PRI = (1 × 8) + 6 = 14

So the raw syslog message would start with `<14>`. 
A SIEM receiving that knows immediately what type of 
message it is without reading the text at all.

The bigger insight from today is the centralization 
problem. My Kali VM generates syslog. My Ubuntu VM 
generates syslog. My Windows host generates XML event 
logs. My router probably generates vendor-specific 
syslog with different field names. Each one needs a 
different collection method before a SIEM can even 
see them. The SIEM is the end of the pipeline — if 
the pipeline is broken, the SIEM is useless.

## Assumption I Made

I assumed all devices on a network naturally speak 
syslog and a SIEM just listens on UDP 514 and collects 
everything. That's wrong. Windows doesn't speak syslog 
at all natively — it needs an agent like Winlogbeat 
to translate event logs and forward them. Cloud 
environments don't push logs to you — you have to 
poll their APIs to pull them. The collection problem 
is more complex than I expected before today.

## Uncertainty I Have

I understand the collection architecture on paper now 
but I haven't actually built any of it. When I get to 
Month 2 and start working with Splunk or Elastic, 
I want to set up an actual forwarder from Ubuntu to 
a central collector and see what happens when the 
forwarder goes offline — does the SIEM notice? Does 
it alert? Or does it silently stop receiving logs 
and nobody knows until an incident happens? That gap 
is what I want to test.