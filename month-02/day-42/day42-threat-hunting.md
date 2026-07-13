# Day 42 — Threat Hunting Methodology

**Date:** 2026-06-23
**Lab status:** Windows VM still down. Hunt hypotheses and methodology documented. Query execution pending lab rebuild.

---

## Hunting vs Alerting — The Mindset Shift

Before today I thought of detection as reactive — something happens, an alert fires, an analyst investigates. That's the alert-response model and it's what most Tier 1 SOC work is.

Threat hunting is different. You don't wait for an alert. You start with a question: "What if X is happening in our environment right now and we just haven't detected it yet?" Then you go looking for evidence of X whether or not any alert has fired.

The distinction matters because alerts only catch what your detection rules are designed to catch. An attacker who avoids triggering your existing rules is invisible in an alert-response model. Hunting goes looking for attacker behaviour that your rules haven't been written for yet.

The other thing that shifted: a hunt doesn't have to find something to be valuable. "I hunted for WMI-based lateral movement and found nothing" is a useful result. It either means there's no WMI-based lateral movement happening (confidence) or it means your telemetry has a gap that would miss it (blind spot discovery). Both are worth knowing.

---

## The Hunting Process

Every hunt follows the same structure:

1. **Hypothesis** — "What if X is happening?"
2. **Data source** — What telemetry would show evidence of X?
3. **Query** — How do I search for that telemetry?
4. **Analysis** — What do the results actually mean?
5. **Refinement** — What legitimate activity looks like X? How do I filter it out?
6. **Documentation** — What did I find, what did I rule out, what are the remaining gaps?

The hypothesis has to be specific enough to be searchable. "What if attackers are in our environment?" is not a hypothesis — it's a feeling. "What if an attacker is using scheduled tasks created outside business hours pointing to files in user-writable directories?" is a hypothesis you can actually search for.

---

## What I Concluded

Hunting is structured curiosity — not random searching, not waiting. You form a belief about what an attacker might be doing, then design a search that would prove or disprove that belief. The methodology matters as much as the technical skill because without it you're just browsing logs hoping to stumble on something.

The brutal mentor note in the roadmap is accurate: alert response is Tier 1. Hunting is what gets you out of Tier 1. Anyone can watch a queue and work tickets. Building hypotheses, designing hunts, and executing them methodically requires a different kind of thinking — one that models attacker behaviour rather than just matching known patterns.

---

## Assumption I Made

I assumed that threat hunting was about finding active threats. It's actually about building confidence in your detection coverage. Most hunts find nothing — not because there's nothing there, but because the hypothesis was wrong or the attacker isn't using that technique. Finding nothing still tells you something: either the environment is clean of that technique, or your telemetry has a gap. The gap discovery is often more valuable than the threat discovery.

---

## Uncertainty I Have

I don't know how to prioritise which hypotheses to hunt first in a real environment. There are unlimited things you could hypothesise about. The answer probably involves threat intelligence — hunting for techniques that threat actors targeting your industry are known to use — but I don't have a systematic framework yet for turning threat intel into a prioritised hunt list. That's something Month 2 needs to address.