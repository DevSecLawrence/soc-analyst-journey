# Day 14 - Elastic/Kibana Comparison Notes

Full write-up: [day14-full-analysis.md](./day14-full-analysis.md)

## Setup Snapshot

- Platform used: Elastic Cloud (Serverless) — Security project (trial)
- Region: GCP — us-central1 (Iowa)

What I actually had data-wise (in my screenshots):
- `Kibana Sample Data Logs` (web logs)

What I actually built:
- a Threshold detection rule for failed authentication

## What I Concluded

Elastic can absolutely do “SIEM thinking” like Splunk, but I had to adjust how I work.

- Splunk: I ask questions in one place (SPL) and the pipeline (`|`) makes it easy to go from raw → stats → timechart.
- Elastic: I filter in KQL, then I often use Kibana UI (Discover / Field statistics / Lens / Rules) to do the rest.

The biggest win today was seeing I can recreate the same detection idea (failed auth → threshold) in a different SIEM.

## Assumption I Made

I assumed KQL would feel like SPL and I’d be able to “pipe” into stats/timecharts the same way. But KQL is mostly filtering, and then Kibana’s UI is where the rest happens (Discover / field stats / Lens / Detection rules).

## Uncertainty I Have

When should I use KQL vs Lucene vs Elasticsearch DSL/ES|QL?

I can filter fine with KQL, but I want to know when I should stop forcing it and move to:
- KQL (simple filters)
- ES|QL / DSL (deeper analysis)

## Screenshots I Captured

- Elastic Cloud home / project created:
	- ![Elastic Cloud home](screenshots/Screenshot%202026-05-28%20120159.png)
- Discover showing events (KQL filters working):
	- ![Discover filter response 404](screenshots/Screenshot%202026-05-28%20182243.png)
	- ![Discover filter by client IP](screenshots/Screenshot%202026-05-28%20182513.png)
	- ![Discover time-range filter attempt](screenshots/Screenshot%202026-05-28%20182850.png)
- Detection rule creation (threshold for failed authentication):
	- ![Create new detection rule](screenshots/Screenshot%202026-05-28%20123305.png)
- Detection rule saved/enabled:
	- ![Rule overview](screenshots/Screenshot%202026-05-28%20180353.png)

## Brutal Reality Check (what I still need)

Right now, the screenshots clearly prove I can:
- navigate Kibana
- run KQL filters in Discover
- build a SIEM threshold detection rule

What I still want (so this isn’t just “sample data practice”) is proof from *my own* security logs (auth.log / syslog / Windows Security events), not just sample data.

So next time I need screenshots that show:
- Fleet agent enrolled + Healthy (or whatever integration path I use)
- Discover showing my own auth failures (ECS fields like `event.category:authentication` and `event.outcome:failure`)
- Rule execution results or an alert firing
