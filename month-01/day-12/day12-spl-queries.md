# Day 12 - SPL Examples

## Quick queries to paste into Splunk

1) Find events from a specific source:
```
index=main source="/var/log/auth.log" | head 20
```

2) Search for a specific IP:
```
index=* "192.0.2.1" | table _time host source sourcetype
```

3) Count events by sourcetype:
```
index=* | stats count by sourcetype
```

4) Top 10 source IPs:
```
index=* | top limit=10 src_ip
```

5) Brute-force detection example (start point):
```
index=main sourcetype=auth | bin _time span=5m | stats count(eval(action="failure")) as failures by _time src_ip user | where failures>10
```


