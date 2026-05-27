# Day 13 — Splunk Detections: From “I Did It” to “Splunk Sees It”

## What I Concluded

Today was me proving (to myself) that I can:

1) generate a real security signal on the box,
2) confirm it exists in the raw log (`/var/log/auth.log` / `/var/log/syslog`), and
3) validate that Splunk is ingesting my log sources, then start shaping those logs into something I can detect on.

This is the part where SIEM stops being “cool dashboards” and turns into: *can I take messy logs and turn them into something I can detect on?*

---

## What I Did (Quick Timeline)

- Simulated failed SSH logins locally (invalid user + wrong password).
- Verified the failures were written to `auth.log`.
- Queried my ingested auth/syslog data in Splunk (`index=main`) and explored different ways of grouping/correlating events.
- Switched over to `syslog` and started measuring which processes were generating the most noise over time.

---

## Step 1 — Generate the “Attack” (Failed SSH Attempts)

I basically spammed SSH attempts against `localhost` using a fake username (`wronguser`). The goal wasn’t to “hack” anything — it was to create failed-auth events on purpose so I’d have something to hunt.

![Generating failed SSH login attempts](screenshots/Screenshot%20from%202026-05-27%2020-45-22.png)

What matters here:
- This is the same mindset as a real SOC workflow: create or observe an event → confirm it’s logged → confirm the SIEM sees it.

---

## Step 2 — Verify the Raw Log (auth.log)

Before trusting Splunk, I checked the source-of-truth: `auth.log`.

I grepped for the strings that usually show up during SSH failures: `Failed` and `Invalid`.

![Confirming failed SSH events in /var/log/auth.log](screenshots/Screenshot%20from%202026-05-27%2020-48-37.png)

What I noticed:
- The events clearly show `Invalid user wronguser` and `Failed password for invalid user wronguser`.
- Source IP is `127.0.0.1` because I attacked from the same machine.
- I also saw a `sudo:` entry for the grep command itself — which is a reminder that *admin actions leave footprints too*.

---

## Step 3 — Validate It in Splunk (linux_auth)

At this point I’m thinking: “Okay, the box logged it… now can I actually *find it fast* in Splunk?”

### Proof query (the missing screenshot to make this airtight)

Right now, my screenshots prove Splunk is ingesting `linux_auth` and `syslog`. What I still want (for a clean evidence chain) is one screenshot that shows the exact SSH failure strings (`wronguser` / `Failed password` / `Invalid user`) *inside Splunk*.

Run this in Splunk and capture a screenshot of the Events view:
```
index=main sourcetype="linux_auth" (wronguser OR "Failed password" OR "Invalid user")
| table _time host source sourcetype _raw
```

If that returns nothing, widen the time range to `All time`, then try:
```
index=main sourcetype="linux_auth" sshd ("Failed password" OR "Invalid user")
| head 50
```

Screenshot to capture (save into `screenshots/`):
- `Screenshot - splunk proof wronguser.png` (name can be anything, but include “proof” so it’s easy to find later)

### Correlation attempt: group events by user (transaction)

I tried using `transaction` to group related auth events together by `user`.

Query I ran (as shown in the screenshot):
```
index=main sourcetype="linux_auth"
|transaction user maxspan
|where eventcount > 1
|table _time, user, eventcount, duration
```

![Transaction query results grouped by user](screenshots/Screenshot%20from%202026-05-27%2021-02-03.png)

What I learned from this:
- `transaction` is powerful, but it’s also easy to “accidentally” create huge transactions.
- My `duration` came back *massive* (hundreds of thousands of seconds). That’s a clue that I grouped events over too wide a time window.

Also, I didn’t set a real `maxspan` value in the first attempt — that’s on me. For anything detection-ish, I should always put a tight time window.

If I wanted this to behave more like a real detection window, I’d tighten it up like:
```
index=main sourcetype="linux_auth" ("Failed password" OR "Invalid user")
|transaction user maxspan=5m
|where eventcount > 3
|table _time, user, eventcount, duration
```

### Sanity check: look at raw events and fields

I also opened the Events view to confirm fielding and context: host, source file path, and sourcetype.

![Events view showing linux_auth fields and raw event context](screenshots/Screenshot%20from%202026-05-27%2021-02-11.png)

What I liked here:
- I can see `host=ubuntu`, `source=/var/log/auth.log`, `sourcetype=linux_auth`.
- This is where you verify you’re not chasing the wrong dataset.

---

## Step 4 — Measure Noise in syslog (Which Processes Spam Events?)

Then I switched gears to `syslog` and started asking a SOC-style question:

“Which processes are the loudest, and how fast are they generating events?”

Query I ran (as shown in the screenshot):
```
index=main sourcetype="syslog"
|stats count, earliest(_time) as first_seen, latest(_time) as last_seen by process
|eval duration_mins = round((last_seen - first_seen)/60, 2)
|eval avg_events_per_min = round(count/duration_mins, 2)
|sort -avg_events_per_min
|head 10
```

![Stats + eval to calculate average events per minute by process](screenshots/Screenshot%20from%202026-05-27%2021-15-38.png)

What I learned:
- `stats` + `eval` is where Splunk starts to feel like a real analysis tool.
- `earliest(_time)` / `latest(_time)` came back as epoch values in my table — that’s normal, but if I want readable timestamps I’d convert them:
```
|eval first_seen_readable=strftime(first_seen, "%F %T"), last_seen_readable=strftime(last_seen, "%F %T")
```

---

## Step 5 — Try to Combine Datasets (join)

I started experimenting with `join` because the idea is simple:

“Can I compare activity by user across different log sources?”

Here’s the join-style query attempt captured in my screenshots:

![Join query attempt in Splunk](screenshots/Screenshot%20from%202026-05-27%2021-25-40.png)

![Join query attempt (zoomed view)](screenshots/Screenshot%20from%202026-05-27%2021-25-47.png)

This is the corrected version of what I was aiming for (auth vs syslog):
```
index=main sourcetype="linux_auth"
|stats count as auth_count by user
|join user [ search index=main sourcetype="syslog" | stats count as syslog_count by user ]
|table user, auth_count, syslog_count
|sort -auth_count
```

Main takeaway:
- Correlation is not just “one query” — it’s making sure you’re actually joining the right sources, on the right key.

---

## Extra Evidence — syslog raw events

I also grabbed a screenshot showing raw syslog events and fields (AppArmor denies, cron, etc.).

![Raw syslog events and extracted fields](screenshots/Screenshot%20from%202026-05-27%2021-25-59.png)

---

## What I Learned (In Plain Terms)

- I can’t just “trust Splunk” — I need to validate the raw logs first.
- Creating the event on purpose (failed SSH) made everything click. I controlled the input, then verified the output.
- `transaction`, `stats`, `eval`, and `join` are the tools that move me from “searching” to “detecting.”
- Time windows matter. If I don’t constrain them, I can accidentally make results look weird (huge durations, grouped events that shouldn’t be grouped).

---

## What I’d Do Next (Turning This Into a Real Alert)

Now that I can generate the failed SSH signal and verify it in `auth.log` (and Splunk is ingesting my sources), the next move is:

1) Save the search as an alert.
2) Schedule it (ex: every 5 minutes).
3) Trigger when `count > 0` (lab) or `count > N` (real world).
4) Add an action (Triggered Alerts list / email / webhook).

---
