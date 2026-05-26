# Day 12 — SPL Examples (cheat sheet)

## Quick checks

1) Show 10 events (sanity check):
```spl
index=* | head 10
```

2) Find events from a specific source:
```spl
index=main source="/var/log/auth.log" | table _time host source sourcetype _raw | head 20
```

3) Search for a specific IP:
```spl
index=* "192.0.2.1" | table _time host source sourcetype src_ip dest_ip user message
```

4) Count events by sourcetype:
```spl
index=* | stats count by sourcetype
```

5) Top 10 source IPs:
```spl
index=* | top limit=10 src_ip
```

6) Timechart of events (1h buckets):
```spl
index=* | timechart span=1h count
```

## Brute-force detection starter

```spl
index=main sourcetype=auth OR sourcetype=linux_auth
| eval fail=if(action=="failure" OR result=="failure" OR status=="FAIL",1,0)
| bin _time span=5m
| stats sum(fail) as failures dc(user) as users by _time src_ip
| where failures > 10
| sort - failures
```

Notes:
- Adjust field names (`action`, `result`, `status`) to match your dataset.
- Use `table _time src_ip users failures` to present final results.

## Parsing tips
- Use `rex` to extract fields from `_raw` when Splunk didn't extract them:
```spl
| rex field=_raw "(?i)(?<src_ip>\b\d{1,3}(?:\.\d{1,3}){3}\b)"
```
- `eval` can normalize values, e.g., lowercase a field: `| eval user=lower(user)`

## From query to alert
- Save the working detection query as a saved search.
- Configure a schedule (e.g., run every 5 minutes) and an action (email or webhook).
- Start with `throttle` or higher thresholds to avoid floods of alerts.
