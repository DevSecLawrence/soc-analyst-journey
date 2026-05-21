# Day 09 - Windows Event Log Deep Dive

Capture and analyze key Windows Event IDs, then document what the log fields actually tell you.

## What I did (beginner version)

- Opened Event Viewer → Windows Logs → Security
- Filtered the log for `4624`, `4625`, `4688`
- Clicked a few events and read the General tab
- Exported the filtered log to an `.evtx` file

## What I noticed from my screenshots

- Filtering by Event ID made the huge Security log way easier to read.
- `4624` = a successful logon (it literally says “successfully logged on”).
- `4688` = a new process was created.

## Screenshots (you can view them here)

![Filter Current Log](./screenshots/Screenshot%202026-05-21%20173625.png)

![Example 4624](./screenshots/Screenshot%202026-05-21%20173833.png)

![Example 4688](./screenshots/Screenshot%202026-05-21%20173935.png)

## Files

* [Full Analysis](./day09-windows-events.md)
* [Event Samples](./event-samples/)
* [Screenshots](./screenshots/)
