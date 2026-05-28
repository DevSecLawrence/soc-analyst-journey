# Day 14 - Splunk vs Elastic (What’s Easier / What’s Harder)

Full write-up: [day14-full-analysis.md](./day14-full-analysis.md)

## My Goal

Recreate the same investigation logic in two SIEMs (and be honest about what felt better/worse):
- Splunk (SPL)
- Elastic (KQL + Kibana + Detection rules)

## What Was Easier in Elastic

- Spinning up a SIEM UI fast: Elastic Cloud Serverless got me into Kibana quickly.
- Turning a detection idea into a rule: the Detection Rule wizard made it straightforward to create a threshold rule.
- Visual feedback: Discover + histograms made it easy to sanity-check “do I even have events?”

## What Was Harder in Elastic

- Field names and normalization: I had to pay attention to which data view I’m in and what fields exist.
- KQL is mostly filtering: for “stats-like” work I naturally wanted SPL-style pipes, but in Elastic I often have to switch to Lens/Field statistics/Rules.
- Writing a *correct* brute-force threshold: if I don’t group by a field like `source.ip`, I can accidentally alert on the total failures across everything.

## What Was Easier in Splunk

- One language for everything: SPL lets me go from raw events → parsing → aggregations in one query.
- Fast ad-hoc investigations: `stats`, `timechart`, and chaining commands is really smooth.

## What Was Harder in Splunk

- Building “productized” detections can take more discipline (naming, scheduling, thresholds, tuning) — it’s easy to stay in exploration mode.
- Depending on the environment, ingestion/onboarding can be more manual compared to a guided cloud setup.

## Syntax Differences I Noticed

- Pipes vs UI-driven aggregations
- Field naming / normalization
- How time windows are applied

## My “SIEM-Agnostic” Lesson

The tool changes, but the thinking doesn’t: start from evidence (do I have the right events?), ask a tight question, filter hard, then define a threshold that matches attacker behavior (count + time window + group-by). A “brute force” detection isn’t just “lots of failures” — it’s “lots of failures from the same source in a short window,” and that logic matters whether I write it in SPL or build it in a Kibana rule.

## Screenshots (proof)

- ![Elastic Cloud home](screenshots/Screenshot%202026-05-28%20120159.png)
- ![Create detection rule](screenshots/Screenshot%202026-05-28%20123305.png)
- ![Rule overview enabled](screenshots/Screenshot%202026-05-28%20180353.png)
- ![Discover KQL filters](screenshots/Screenshot%202026-05-28%20182243.png)
