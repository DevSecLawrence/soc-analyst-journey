# Day 12 — Splunk Fundamentals

## 🎯 Primary Focus
Learn basic Splunk SPL: searching, filtering, and simple statistics.

## Medium Exercise
1. Install Splunk Free or use Splunk Cloud trial.
2. Load BOTS dataset or your sample logs.
3. Run these queries and record results:
   - `index=* sourcetype=* | head 10`
   - `index=* "specific_ip_or_string" | table _time host source sourcetype` 
   - `index=* | stats count by sourcetype`
   - `index=* | timechart count by sourcetype span=1h`

## Hard Exercise
1. Using the dataset, find authentication failures and count by source IP in 5-minute windows.
2. Build a query that groups by source IP and target account, counts failures, and filters counts > 10 in a 5-minute window.

## What I Concluded


## Assumption I Made


## Uncertainty I Have

