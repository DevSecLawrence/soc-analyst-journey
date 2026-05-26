# Day 12 — SPL Query Reference

All queries run against index=main with real lab 
logs from Ubuntu VM (syslog + auth.log).

---

## Foundational Queries

### Q1 — View raw events
index=main | head 20
- `index=main` — which dataset to search
- `head 20` — limit to first 20 results
- Use this first to confirm data is loaded

---

### Q2 — Count events by sourcetype
index=main | stats count by sourcetype | sort -count
- `stats count by sourcetype` — group and count
- `sort -count` — highest first (- means descending)
- Use this to understand what data you have before 
  writing investigation queries

---

### Q3 — Filter by sourcetype
index=main sourcetype=linux_auth | head 20
- `sourcetype=linux_auth` — only auth.log events
- Combine with keywords to narrow further
- Every query should have a sourcetype filter when 
  possible — faster and more precise than searching 
  everything

---

### Q4 — Event distribution over time
index=main | timechart span=1h count
- `timechart` — always plots against time
- `span=1h` — bucket events into 1-hour chunks
- Switch to Visualization tab to see the graph
- Use this to find when activity spiked

---

## Investigation Queries

### Q5 — Top source IPs by volume
index=main | stats count by src_ip | sort -count | head 10
- Works on network logs (firewall, proxy, web)
- The top IP by volume is often the attacker
- A massive gap between #1 and #2 is anomalous

---

### Q6 — Find all sudo usage
index=main sourcetype=linux_auth sudo | head 20
- Searches for the word "sudo" in auth.log events
- Shows who ran sudo, what command, from where
- Linux equivalent of Windows Event ID 4688

---

### Q7 — Failed SSH login attempts
index=main sourcetype=linux_auth "Failed password" |
stats count by host
- "Failed password" is the exact string in auth.log
- Use quotes for exact phrase matching in SPL
- In production this query returns hundreds of hits 
  from automated internet scanners

---

### Q8 — Table view of web requests
index=main sourcetype=apache_access |
table _time, src_ip, uri_path, status, useragent
- `table` picks specific fields to display
- `_time` is Splunk's internal timestamp field
- Use this instead of raw events for readability

---

## SPL Pipeline Pattern

Every SPL query follows this structure:
index=X sourcetype=Y keyword | command1 | command2

- Everything flows left to right through the pipe
- Each command processes the output of the previous
- index and sourcetype always go first
- Filter before you transform — faster searches

---

## Key Commands Reference

| Command | What it does | Example |
|---|---|---|
| head | Limit results | head 20 |
| stats count by | Group and count | stats count by user |
| sort | Order results | sort -count |
| timechart | Plot against time | timechart span=1h count |
| table | Pick fields to show | table _time, src_ip |
| where | Filter after stats | where count > 100 |
| dedup | Remove duplicates | dedup src_ip |
| eval | Create new fields | eval gb=bytes/1024/1024 |