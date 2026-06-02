# Day 19 — TryHackMe SOC Level 1: First Labs

## Rooms Completed

1. Pyramid of Pain
2. Traffic Analysis Essentials

---

## Room 1 — Pyramid of Pain

### What Was New

The pyramid structure itself was new to me. I knew
IOCs existed but I never thought about them in terms
of how much pain blocking each type causes an
attacker.

Hash values are at the bottom — easiest for defenders
to block, easiest for attackers to change. One
recompile and the hash is different. IP addresses
are slightly harder but still trivial to rotate.
Domain names take a bit more effort. The higher you
go — TTPs at the top — the more you hurt the
attacker because you're forcing them to change how
they operate, not just what files they use.

That reframing hit differently. A lot of detection
work focuses on hashes and IPs. The pyramid says
that's the least effective place to focus if you
want to actually slow someone down.

### Where Days 1-18 Helped

Day 15 MITRE ATT&CK work connected directly here.
TTPs at the top of the pyramid map exactly to
ATT&CK techniques. When I read about T1059
(PowerShell) or T1078 (Valid Accounts) on Day 15,
I was already learning what sits at the top of the
pyramid without knowing the framework by name.

### Mistakes I Made

I initially thought network artifacts and host
artifacts were the same thing. The room clarified
that network artifacts are things like suspicious
user-agent strings or URI patterns in traffic —
things you'd see in Wireshark. Host artifacts are
registry changes, files dropped, processes spawned —
things you'd see in EDR or Windows Event Logs.
Same investigation, different data sources.

---

## Room 3 — Traffic Analysis Essentials

### What Was New

The room introduced Zeek and NetworkMiner alongside
Wireshark. I've only used Wireshark so far. Zeek
is interesting because it doesn't capture raw
packets — it generates structured logs from traffic.
Instead of reading packet-by-packet, you get
conn.log, dns.log, http.log already parsed and
ready to query. That's closer to what a real SOC
uses because reading raw PCAPs at scale is not
practical.

NetworkMiner extracts artifacts from PCAPs
automatically — files, credentials, images,
certificates. Instead of manually following HTTP
streams in Wireshark to find what was transferred,
NetworkMiner pulls it out directly.

### Where Days 1-18 Helped

Days 3 through 7 were basically this room but
done manually. DNS filtering in Day 3, ARP analysis
in Day 4, ICMP in Day 5, HTTP in Day 6, TLS in
Day 7 — the room covered all of those concepts but
in a faster format. The difference is I'd already
done them hands-on so the questions made sense
immediately instead of feeling abstract.

The room felt easier than it probably should because
of the Wireshark work I'd already done. That was
a good sign.

### Mistakes I Made

I tried to answer questions about traffic types
from memory instead of actually opening the PCAP
and checking. Got one wrong because of that. The
lesson is that even when you think you know, verify
in the data. That's the whole point of being an
analyst — you don't guess, you look.

---

## What I Concluded

The gap between self-study and labs is real but
it goes both ways. Some things were harder in
the lab than they seemed in theory. Some things
were easier because I'd already done the hands-on
work from Days 1-18.

The Pyramid of Pain room changed how I think about
detection priorities. I've been focused on IOC
types that are easy to block but also easy to
rotate. The pyramid says the highest-value
detections target attacker behavior, not attacker
artifacts. That reframes what I should be building
toward in Month 2 when I write detection rules.

The Kill Chain room connected the theory from
Day 15 (MITRE ATT&CK) and Day 18 (IR lifecycle)
into one coherent picture. Attacks are stories
with stages. IR is the response to those stages.
ATT&CK is the vocabulary for describing the
techniques within each stage.

## Assumption I Made

I assumed TryHackMe rooms would cover new ground
that I hadn't seen yet. A lot of it was review —
but that's not a bad thing. It meant I could move
faster and spend more mental energy on the parts
that were actually new rather than struggling with
foundations. The assumption to update is that
labs are for learning new things. Sometimes they're
for confirming you actually know what you think
you know. That confirmation matters.

## Uncertainty I Have

The rooms have one right answer. Real investigations
don't. When I was answering questions in the Traffic
Analysis room, I sometimes had two interpretations
of the same packet and had to pick one. In a real
investigation both interpretations would need to
be documented and investigated. I don't know yet
how to handle ambiguity at scale — when you have
10,000 events and multiple possible explanations
for the same behavior, how do you decide which
thread to pull first? That's what I want to
develop in Month 2.