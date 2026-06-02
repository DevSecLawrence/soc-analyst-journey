# Day 19 — Analyst Notes: Pyramid of Pain
**Room:** Pyramid of Pain (TryHackMe SOC Level 1)
**Date:** Day 19 of 180
**Analyst:** DevSecLawrence
**Format:** Professional investigation notes

---

## 1. Scenario

The room presented a series of IOC types and asked
me to classify them within the Pyramid of Pain
framework — a model developed by David Bianco that
ranks IOCs by how much effort it costs an attacker
to change them when defenders block them.

The task was to understand why some IOCs are more
valuable than others for long-term detection, and
to correctly identify which category each IOC type
belongs to.

---

## 2. Investigative Steps Taken

**Step 1 — Understood the framework structure**

Mapped the 6 levels bottom to top:
- Hash values (trivial to change)
- IP addresses (easy to change)
- Domain names (simple to change)
- Network/host artifacts (annoying to change)
- Tools (challenging to change)
- TTPs (tough to change — requires attacker to
  rethink their methodology)

**Step 2 — Worked through each question by
applying the framework**

For each IOC presented, asked: how long would it
take an attacker to replace this if I blocked it?
Seconds to minutes = bottom of pyramid. Days to
weeks or requires learning new techniques = top.

**Step 3 — Cross-referenced with Day 15 knowledge**

TTPs at the top of the pyramid are the same as
ATT&CK techniques. T1059 (PowerShell execution)
is a TTP. If I detect and block PowerShell abuse
specifically, the attacker has to switch to a
different execution method — that costs them time,
testing, and potentially exposes them again during
the transition.

**Step 4 — Identified the mistake on network vs
host artifacts**

Initially classified a user-agent string as a
host artifact. Corrected after re-reading — user-
agent strings travel in HTTP headers captured in
network traffic, making them network artifacts.
Host artifacts are things left on the endpoint
itself: registry keys, dropped files, spawned
processes.

---

## 3. Conclusion

The Pyramid of Pain is a prioritization framework
for detection engineering. Detections built on
hash values and IP addresses are easy to maintain
but provide weak protection — attackers rotate
these constantly. Detections built on TTPs are
harder to build and tune but force attackers to
fundamentally change how they operate.

For a SOC analyst this means two things. First,
don't dismiss hash and IP detections — they catch
lazy attackers and opportunistic malware. Second,
don't rely on them for targeted threats where the
attacker has resources and motivation to evade.
Targeted threat actors change infrastructure fast.
Their TTPs change slowly.

---

## 4. Confidence Level

**High** for the classification of IOC types and
the framework logic.

**Medium** for correctly distinguishing network
vs host artifacts in edge cases — some artifacts
can appear in both depending on how you collect
them.

**Low** for knowing when to prioritize TTP-based
detection over IOC-based detection in a real
environment with limited analyst bandwidth. The
framework tells you what's more valuable. It
doesn't tell you how to allocate limited time.

---

## 5. What I Would Do Next If This Were Real

If I was applying this framework to a real
environment:

1. Audit existing detection rules — classify each
   one by pyramid level. What percentage are hash/IP
   detections vs TTP detections?

2. Identify the top 3 TTPs most relevant to our
   threat profile — based on which threat actors
   target our industry and what their common
   techniques are (from MITRE ATT&CK Groups section).

3. Build one TTP-based detection rule per sprint
   focused on behavior, not artifacts. For example:
   instead of blocking a specific PowerShell hash,
   detect encoded PowerShell execution from Office
   applications regardless of which specific binary
   is used.

4. Keep hash and IP detections running but move
   them to lower-priority alert queues — useful
   for catching low-sophistication threats without
   consuming Tier 1 analyst time on high-priority
   investigations.