# Day 14 - KQL Query Notes (Translated from SPL)

This file is where I map “the question I asked in Splunk” to “how I ask the same question in Elastic/Kibana”.

## Data Notes

- Time field: `@timestamp`
- Common fields I used:
  - `message`
  - `event.dataset` / `data_stream.dataset`
  - `host.name`
  - `source.ip`
  - `user.name`

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

---

### 3) Count by source type

**SPL**
```
index=main | stats count by sourcetype | sort -count
```

**KQL**

KQL filters the dataset; for counts I used Lens / field statistics:
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

Then build the threshold logic in:
- Elastic Security Detection Rule (Threshold rule), OR
- Kibana Rules (Elasticsearch query rule)
