# Day 14 - KQL Query Notes (Translated from SPL)

Full write-up: [day14-full-analysis.md](./day14-full-analysis.md)

This is me mapping “what I’d normally ask in Splunk” to “how I asked it in Elastic/Kibana.”

## Data Notes

- Time field: `@timestamp`
- Common fields I used:
  - `message`
  - `event.dataset` / `data_stream.dataset`
  - `host.name`
  - `source.ip`
  - `user.name`

In my screenshots, I was using the `Kibana Sample Data Logs` data view, so field names looked like:
- `clientip`
- `response`

That was a good reminder: same investigation idea, totally different field names depending on the dataset.

---

## Foundational Queries (Day 12 equivalents)

### 1) Find all events from a specific source

**SPL**
```
index=main sourcetype=linux_auth | head 20
```

**KQL (Discover filter examples)**
```
event.dataset : "system.auth"
```

---

### 2) Filter by IP address

**SPL**
```
index=main src_ip=1.2.3.4
```

**KQL**
```
source.ip : "1.2.3.4"
```

Fallback if IP isn’t extracted:
```
message : "1.2.3.4"
```

**KQL I actually ran (screenshot evidence)**
```
clientip : "117.165.135.88"
```

Screenshot:
- ![Discover filter by clientip](screenshots/Screenshot%202026-05-28%20182513.png)

---

### 3) Count by source type

**SPL**
```
index=main | stats count by sourcetype | sort -count
```

**KQL**

KQL filters the dataset; for counts I leaned on Lens / field statistics:
- Field: `event.dataset` (or `data_stream.dataset`)
- Metric: Count of records

---

### 4) Time-range search

**SPL**
```
index=main earliest=-24h
```

**Elastic**

Use the Kibana time picker (top right):
- `Last 24 hours`, `Last 7 days`, `All time`

You can also filter by time in the query bar (works, but the time picker is usually cleaner):

**Attempt I captured (screenshot evidence)**
```
@timestamp >= "2026-05-28" and @timestamp <= "2026-05-28"
```

**Cleaner “one day” version**
```
@timestamp >= "2026-05-28" and @timestamp < "2026-05-29"
```

I’m calling this out because “<= same day” can be confusing. Using `< next day` is easier to reason about.

Screenshot:
- ![Discover timestamp range filter](screenshots/Screenshot%202026-05-28%20182850.png)

---

## Extra KQL Filters I Ran (screenshots)

### Filter by HTTP response code
```
response : "404"
```

Screenshot:
- ![Discover response 404 filter](screenshots/Screenshot%202026-05-28%20182243.png)

---

## Hard Detection Query (Day 13 equivalent)

Goal: brute-force style detection.

**SPL idea**
```
"Failed password" | stats count by src_ip
```

**KQL filter idea**
```
message : "Failed password"
```

**KQL filter shown in my rule creation screenshot (more ECS-style)**
```
event.category : "authentication" and event.outcome : "failure"
```

Screenshot:
- ![Create new detection rule with failed-auth filter](screenshots/Screenshot%202026-05-28%20123305.png)

Rule created:
- ![Rule overview](screenshots/Screenshot%202026-05-28%20180353.png)

Then build the threshold logic in:
- Elastic Security Detection Rule (Threshold rule), OR
- Kibana Rules (Elasticsearch query rule)
