# Day 12 — Splunk Fundamentals: First Queries on Real Data

## What I Concluded

Today was a full battle before I even wrote one query.

Network was 45Kbps. BOTS dataset download was going to 
take 11 hours. Disk space was at 85%. Splunk kept 
refusing to run searches. USB transfer corrupted the 
file. Shared folder permissions were denied.

But eventually I got it working — loaded my own real 
logs from previous days into Splunk and ran 8 SPL 
queries against them. Not a pre-made dataset. My own 
lab data.

The three sources I loaded:
- /var/log/syslog — Ubuntu system log
- /var/log/auth.log — authentication events
- /var/log/apache2/access.log — Apache web server log

Total events indexed: 20,341 across both sources 
(Apache didn't load — more on that below).

## Screenshot Evidence

These were the first two blockers before I got to the queries:

![Internet speed test showing 45 Kbps](screenshots/Screenshot%20from%202026-05-25%2020-32-42.png)

![Splunk download page while I was trying to get the platform installed](screenshots/Screenshot%20from%202026-05-25%2021-36-49.png)

---

## The 8 SPL Queries

### Query 1 — See all events
index=main | head 20
**What it does:** Pulls the first 20 events from the 
main index. Time range was last 24 hours. Returned 
20 events immediately. The first event I saw was an 
AppArmor DENIED entry from the kernel — Firefox's 
MemoryPoller process being blocked from accessing 
/proc/pressure/memory. That's the OS security policy 
doing its job.

**What I learned:** index= is always the starting 
point of any SPL query. head limits the results so 
you don't wait forever on large datasets.

![Query 1 showing raw events in Splunk](screenshots/Screenshot%20from%202026-05-26%2020-17-21.png)

---

### Query 2 — Count events by sourcetype
index=main | stats count by sourcetype | sort -count
**What it does:** Groups all events by their sourcetype 
and counts them. Returns a table sorted by highest 
count first.

**Result:** 20,288 events total. Only syslog and 
linux_auth showed up — apache_access had 0 events 
despite me adding the monitor. The Apache log file 
existed but Splunk didn't pick it up, probably 
because the file had no new writes since I added 
the monitor. Lesson: Splunk monitors for new data 
by default, not historical data unless you configure 
it differently.

**What I learned:** stats count by is the most 
useful command for getting a quick overview of 
what data you actually have before writing 
investigation queries.

![Query 2 showing event count by sourcetype](screenshots/Screenshot%20from%202026-05-26%2020-22-24.png)

---

### Query 3 — Apache events
index=main sourcetype=apache_access | head 20
**Result:** 0 events.

The Apache log monitor wasn't picking up the file. 
This is because Splunk's file monitor only reads 
new lines written after the monitor was added. 
Since I wasn't generating new Apache traffic, 
nothing came through. This is actually an 
important operational lesson — if you add a 
Splunk monitor to an existing log file, you need 
to either configure it to read from the beginning 
or generate new activity.

![Query 3 showing no Apache events returned](screenshots/Screenshot%20from%202026-05-26%2020-24-33.png)

---

### Query 4 — Event distribution by hour
index=main | timechart span=1h count
**What it does:** Splits events into 1-hour buckets 
and counts them. Shows you when activity happened.

**Result:** 20,341 events across 25 hourly buckets. 
The visualization tab showed a pie chart by default. 
I could see the activity was mostly concentrated 
in specific hours — matching when I was actively 
using the Ubuntu VM yesterday and today.

**What I learned:** timechart is different from stats 
— it always plots against time. This is the query 
you run first in an incident to find when activity 
spiked. In a real investigation that spike is your 
attack window.

![Query 4 showing the timechart query result](screenshots/Screenshot%20from%202026-05-26%2020-27-27.png)

![Query 4 visualization showing event distribution by hour](screenshots/Screenshot%20from%202026-05-26%2020-30-17.png)

---

### Query 5 — Top source IPs
index=main | stats count by src_ip | sort -count | head 10
**Result:** Statistics showed 0 results with src_ip 
field. Syslog doesn't have a src_ip field by default 
— that field is specific to network logs like 
firewall or proxy data. The query worked but returned 
nothing because my log sources don't have that field.

**What I learned:** Not every SPL query works on 
every log source. Field names depend entirely on 
what the log source provides. This is why field 
extraction and sourcetype configuration matters 
so much in a real SIEM setup.

![Query 5 showing no src_ip field results](screenshots/Screenshot%20from%202026-05-26%2020-34-18.png)

---

### Query 6 — Sudo usage
index=main sourcetype=linux_auth sudo | head 20
**Result:** 20 events. I could see my own sudo 
commands from earlier today including:
sudo: lawrence : TTY=pts/0 ; PWD=/home/lawrence ;
USER=root ; COMMAND=/opt/splunk/bin/splunk add monitor
/var/log/apache2/access.log -index main -sourcetype
apache_access

That's me adding the Apache monitor showing up in 
auth.log. The auth log recorded exactly what command 
I ran as root, from which directory, and what user 
I was. This is exactly what Day 9 showed on Windows 
with 4688 events — same concept, different OS.

**What I learned:** auth.log is the Linux equivalent 
of Windows Security Event Log for sudo activity. 
Every privileged command leaves a trail here.

![Query 6 showing sudo events from auth.log](screenshots/Screenshot%20from%202026-05-26%2020-35-52.png)

---

### Query 7 — Failed password attempts
index=main sourcetype=linux_auth "Failed password" |
stats count by host
**Result:** 0 events.

No failed SSH login attempts on my Ubuntu VM. That's 
actually expected — SSH wasn't exposed to the internet 
and I didn't try any failed logins. In a real 
environment facing the internet this query would 
return hundreds of results from automated scanners 
within hours of SSH being opened.

**What I learned:** Zero results isn't always a 
problem — sometimes it confirms your environment 
is clean. The value of this query is in production 
environments where failed logins are constant noise 
you need to sort through.

![Query 7 showing zero failed password attempts](screenshots/Screenshot%20from%202026-05-26%2020-36-43.png)

---

### Query 8 — Apache table view
index=main sourcetype=apache_access | table _time,
src_ip, uri_path, status, useragent
**Result:** 0 events — same Apache issue as Query 3.

The query syntax itself is correct. The table command 
picks specific fields to display instead of the full 
raw event. In a working Apache setup this would show 
you every web request in a clean readable format — 
timestamp, who made the request, what page they hit, 
what status code came back, and what browser they 
used.

![Query 8 showing the Apache table query with no results](screenshots/Screenshot%20from%202026-05-26%2020-39-34.png)

---

## The Apache Problem — What Happened

Three queries returned 0 because Apache events never 
loaded. The reason: Splunk's file monitor watches 
for new data written to a file after the monitor 
is added. My Apache log had old data from Day 8 
but no new writes after I added the monitor.

Fix for next time:
```bash
sudo /opt/splunk/bin/splunk add monitor \
/var/log/apache2/access.log \
-index main \
-sourcetype apache_access \
-followTail 0
```

The `-followTail 0` flag tells Splunk to read the 
entire file from the beginning, not just new lines.

I could also just generate new Apache traffic:
```bash
curl http://localhost
curl http://localhost/doesnotexist
```

That would create new log lines that Splunk would 
pick up immediately. I'll do this when I revisit 
the BOTS dataset.

---

## What I Concluded

The biggest thing today wasn't the queries themselves 
— it was realising that Splunk is only as useful as 
the data you feed it. Getting data in correctly is 
harder than writing the queries.

I also learned that SPL follows a consistent pattern:
index=X sourcetype=Y [filter] | command | command

Everything flows left to right through the pipe. 
Each command takes the output of the previous one. 
Once you understand that structure every query 
makes sense.

The sudo query was the most interesting result — 
seeing my own commands from earlier today show up 
as log events in Splunk made everything from Days 
9 and 10 click together. I generated those events 
with auditd and auth.log. Now I'm querying them 
in a SIEM. That's the full pipeline working end 
to end.

## Assumption I Made

I assumed adding a file monitor to Splunk would 
automatically ingest all historical data in that 
file. It doesn't. Splunk monitors for new writes 
by default. This is actually the right default 
for production — you don't want a SIEM reading 
years of old logs every time you add a source. 
But for a lab where you're testing with existing 
files, you need to explicitly tell it to read 
from the beginning.

## Uncertainty I Have

I want to understand how Splunk handles field 
extraction automatically vs manually. Some fields 
like host and sourcetype are automatic. Others 
like src_ip depend on the log format being 
recognised. When Splunk doesn't recognise a 
format, how do you write a custom field extraction? 
That's what I want to figure out when I get the 
BOTS dataset loaded — it has proper network logs 
where src_ip, dest_ip, and uri_path fields should 
all extract automatically.

## Full Screenshot Gallery

If you are viewing this on GitHub, every screenshot below should render directly in the page.

![Screenshot 01](screenshots/Screenshot%20from%202026-05-25%2020-32-42.png)
![Screenshot 02](screenshots/Screenshot%20from%202026-05-25%2021-36-49.png)
![Screenshot 03](screenshots/Screenshot%20from%202026-05-26%2020-17-21.png)
![Screenshot 04](screenshots/Screenshot%20from%202026-05-26%2020-17-34.png)
![Screenshot 05](screenshots/Screenshot%20from%202026-05-26%2020-22-24.png)
![Screenshot 06](screenshots/Screenshot%20from%202026-05-26%2020-24-33.png)
![Screenshot 07](screenshots/Screenshot%20from%202026-05-26%2020-27-27.png)
![Screenshot 08](screenshots/Screenshot%20from%202026-05-26%2020-30-17.png)
![Screenshot 09](screenshots/Screenshot%20from%202026-05-26%2020-34-18.png)
![Screenshot 10](screenshots/Screenshot%20from%202026-05-26%2020-34-24.png)
![Screenshot 11](screenshots/Screenshot%20from%202026-05-26%2020-35-52.png)
![Screenshot 12](screenshots/Screenshot%20from%202026-05-26%2020-35-59.png)
![Screenshot 13](screenshots/Screenshot%20from%202026-05-26%2020-36-43.png)
![Screenshot 14](screenshots/Screenshot%20from%202026-05-26%2020-39-34.png)
![Screenshot 15](screenshots/Screenshot%20from%202026-05-26%2020-41-33.png)
![Screenshot 16](screenshots/Screenshot%20from%202026-05-26%2020-42-36.png)
![Screenshot 17](screenshots/Screenshot%20from%202026-05-26%2020-43-20.png)
![Screenshot 18](screenshots/Screenshot%20from%202026-05-26%2020-51-11.png)
![Screenshot 19](screenshots/Screenshot%20from%202026-05-26%2019-52-05.png)