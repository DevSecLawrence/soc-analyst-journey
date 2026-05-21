
# Day 09 — Windows Event Log Deep Dive

For Day 09 I kept it simple: I opened Windows Event Viewer, filtered the Security log for a few important Event IDs, looked at what the fields say, took screenshots, and exported the events.

## TL;DR

- I filtered the Security log for `4624`, `4625`, and `4688`.
- I looked at examples of `4624` (logon) and `4688` (process creation).
- I exported the filtered events to an `.evtx` file.

## What I actually did

1. Opened **Event Viewer** → **Windows Logs** → **Security**.
2. Clicked **Filter Current Log...** and typed: `4624, 4625, 4688`.
3. Clicked a few events to read the **General** tab (and noticed what fields show up).
4. Exported the filtered events to: `event-samples/day09-4624,4625,4688.evtx`.
5. Saved screenshots so I have proof of what I saw.

## What I noticed from the screenshots (beginner notes)

### 1) Filtering makes the log manageable

Before filtering, the Security log is huge. Filtering by Event ID helped me focus on just the events I care about.

![Filter Current Log](./screenshots/Screenshot%202026-05-21%20173625.png)

### 2) Event ID 4624 = Successful logon

This event literally says **"An account was successfully logged on."**

From the example I clicked:

- **Security ID: SYSTEM** (so the system is the “subject” writing the event)
- **Account Name: LAWRENCE$** (it ends with `$`, which usually means a computer account)
- **Account Domain: WORKGROUP**
- **Computer: Lawrence**

![Example 4624](./screenshots/Screenshot%202026-05-21%20173833.png)

### 3) Event ID 4688 = Process creation

This event says **"A new process has been created."**

In the example I clicked, I can see:

- **Event ID 4688**
- **Task Category: Process Creation**
- **Creator Subject shows SYSTEM**

I didn’t go deep into the Details tab yet — my goal today was just to locate the event and understand the basic meaning.

![Example 4688](./screenshots/Screenshot%202026-05-21%20173935.png)

## What I’m still confused about

- What’s the difference between **Subject** vs **New Logon** fields inside `4624`?
- How do I reliably tell whether a logon is “normal user activity” vs something suspicious just from Event Viewer?
- What are the most important fields in the **Details** tab for `4688`?

## Files

- `event-samples/day09-4624,4625,4688.evtx` — my exported Security events
- `screenshots/` — screenshots of the filter and example events

