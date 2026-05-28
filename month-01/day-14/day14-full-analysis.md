# Day 14 — Elastic/Kibana: Same SOC Thinking, Different SIEM

## What I Concluded

Today was me proving I can take the same investigation mindset I’ve been building in Splunk and apply it in Elastic.

Not gonna lie — Elastic feels *different*. In Splunk I’m used to doing everything inside one SPL query. In Kibana, KQL is mainly filtering, and then I lean on the UI (Discover, charts, rules) to finish the job.

The big win is that I didn’t just “click around.” I actually:
- got into Elastic Cloud and opened a Security project
- ran real KQL filters in Discover and confirmed they return results
- created and enabled a brute-force style threshold detection rule

---

## What I Did (Quick Timeline)

1) Opened Elastic Cloud and verified my Security project exists (trial)
2) Used Kibana Discover to practice KQL filtering
3) Built a threshold detection rule in Elastic Security (SIEM)
4) Wrote down what felt easier/harder vs Splunk

---

## Step 1 — Elastic Cloud Setup Proof

I’m on Elastic Cloud (trial) and I have a Security project created.

![Elastic Cloud home / Security project](screenshots/Screenshot%202026-05-28%20120159.png)

What matters:
- I can get into the platform, and I have a place to work (project + Kibana).

---

## Step 2 — Discover (KQL Filtering Like a SOC)

### A) Filter for a response code (simple but real)

I ran this KQL filter:
```
response : "404"
```

![Discover filter response 404](screenshots/Screenshot%202026-05-28%20182243.png)

What this proved:
- I’m not just staring at dashboards — I can actually pull a slice of data by a specific field/value.

### B) Filter by a client IP

I ran:
```
clientip : "117.165.135.88"
```

![Discover filter by client IP](screenshots/Screenshot%202026-05-28%20182513.png)

What I noticed:
- In this data view (`Kibana Sample Data Logs`), the field is `clientip` (not `source.ip`).
- This is exactly why field normalization matters. Same “idea,” different field names.

### C) Time filtering

I also tried filtering time inside the query bar:
```
@timestamp >= "2026-05-28" and @timestamp <= "2026-05-28"
```

![Discover timestamp filter attempt](screenshots/Screenshot%202026-05-28%20182850.png)

Honest takeaway:
- It’s way cleaner to use the time picker, but this helped me understand how time logic works in KQL.
- If I do this again, I’ll use a safer version like:
```
@timestamp >= "2026-05-28" and @timestamp < "2026-05-29"
```

---

## Step 3 — Hard Part: Detection Rule (Threshold)

This is where I switched from “searching” to “detecting.”

### Rule creation

I created a new Elastic Security detection rule.

Key parts visible in my screenshot:
- Rule type: **Threshold**
- Custom query:
  ```
  event.category : "authentication" and event.outcome : "failure"
  ```
- Threshold: **All results >= 10**

![Create new rule](screenshots/Screenshot%202026-05-28%20123305.png)

### Rule saved + enabled

I saved the rule and enabled it.

![Rule overview enabled](screenshots/Screenshot%202026-05-28%20180353.png)

What I like about this:
- This is the same detection logic I’ve been thinking about since Day 13 (failed auth → threshold) but implemented in a different SIEM.

### What’s missing (and I’m not going to pretend it isn’t)

The screenshots do **not** prove alerts fired. And they also don’t prove I grouped by the right field (like `source.ip`).

In brute force, that group-by is everything.

If I leave it as “All results >= 10,” I could end up alerting on the total noise of a whole environment instead of a single attacker/IP.

---

## What I Learned (In Plain Terms)

- Elastic isn’t “hard,” it’s just a different workflow. KQL filters, and then you use Kibana features to do the rest.
- Field names will humble you. The same concept can look totally different depending on dataset and ECS mapping.
- A detection rule isn’t real just because it exists — it’s real when it fires correctly and you can explain why.

---

## What I’d Do Next (To Make This Production-Real)

1) Ingest my own logs (not only sample data): auth logs / Windows Security events / sysmon, etc.
2) Rebuild the rule with a correct group-by (ex: `source.ip`) and a tight time window
3) Trigger it on purpose (generate failed logins) and capture:
   - rule execution results, and/or
   - an actual alert in the Alerts tab

---

## Related Notes

- KQL mapping notes: [day14-kql-queries.md](./day14-kql-queries.md)
- Splunk vs Elastic honest comparison: [day14-splunk-vs-elastic.md](./day14-splunk-vs-elastic.md)
- Setup snapshot + proof screenshots list: [day14-elastic-comparison.md](./day14-elastic-comparison.md)
