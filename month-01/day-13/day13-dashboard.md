# Day 13 — Hard Exercise: Dashboard + Scheduled Reports

Goal: Build an investigation dashboard and schedule a report that triggers an alert when thresholds are met.

Steps (what to click, exact fields):
1. Open Splunk Web → App menu → `Dashboards` → `Create New Dashboard`.
2. Fill fields:
   - Dashboard Title: `Day13 - Investigation Dashboard`
   - ID: `day13-investigation`
   - App: `Search & Reporting`
   - Permissions: `Private` or `Shared in app`
   - Click `Create Dashboard`.
3. Click `Add Panel` → `New` → give Panel Title `Failed Logins by Host`.
4. Paste SPL:
```
index=main sourcetype=linux_auth "Failed password" | stats count by host | sort -count
```
5. Choose Visualization: `Column Chart` or `Table` → `Add to Dashboard`.
6. Add another panel: `Sudo Commands` with:
```
index=main sourcetype=linux_auth sudo | table _time, user, COMMAND
```
7. Add `Event Volume Over Time` panel with:
```
index=main | timechart span=1h count
```
8. Arrange panels by dragging; click `Edit` → panel gear → add descriptions.
9. Save dashboard.

Create a scheduled report (to power alerts):
1. Open the saved search used for a panel → `Save As` → `Report`.
2. Name it `Day13 - Failed Logins Report`.
3. In Reports → select the report → `Edit Schedule`:
   - Enable schedule: `Run every` → `15 minutes`.
   - Actions: `Add to Triggered Alerts` or `Send email`.
4. Save schedule and validate under App → Activity → Jobs.

Capture screenshots:
- Dashboard overview: `screenshot-04-dashboard.png`
- Panel edit modal: `screenshot-05-panel-edit.png`
- Scheduled report config: `screenshot-06-report-schedule.png`
