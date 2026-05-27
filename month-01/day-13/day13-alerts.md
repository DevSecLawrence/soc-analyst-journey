# Day 13 — Medium Exercise: Create a Splunk Alert (Step-by-step)

Goal: Create a scheduled alert that notifies when there are failed SSH login attempts.

Prerequisites: Splunk running and `index=main` ingesting `auth.log` (sourcetype `linux_auth`).

Steps (what to click, exact fields):
1. Open Splunk Web: `http://localhost:8000` and sign in.
2. Click the app selector (top-left) → choose `Search & Reporting`.
3. In the search bar paste:
```
index=main sourcetype=linux_auth "Failed password" | stats count by host
```
4. Set Time range (top-right) → `Last 24 hours` → click the magnifier (Search).
5. Confirm results appear (or 0). Adjust time range if needed.
6. Click `Save As` (top-right of search results) → choose `Alert`.
7. In the Save Alert dialog set:
   - Title: `Day13 - Failed SSH Login Alert`
   - Description: `Alert when any failed SSH login appears in auth.log.`
   - Alert Type: `Scheduled` → `Run every` → `5 minutes` (lab) or `Real-time` if you prefer live detection.
   - Trigger Condition: `If number of results` `is greater than` `0` (or `> 10` to reduce noise).
   - Trigger Actions: enable `Add to Triggered Alerts`; optionally enable `Send email` (requires SMTP configured).
   - Permissions: `Shared in app` if you want others to see it.
8. Click `Save`.
9. Test: go to `Settings` → `Searches, Reports, and Alerts` (or App → Activity → Alerts), find the alert, and click `Run` to execute now.
10. Review `Triggered Alerts` (App → Activity → Triggered Alerts) to see the alert entry.

Capture screenshots for documentation:
- Search results: `screenshot-01-alert-search.png`
- Save Alert dialog filled: `screenshot-02-alert-save.png`
- Triggered Alerts entry: `screenshot-03-alert-triggered.png`
