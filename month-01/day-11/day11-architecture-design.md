# Day 11 - Architecture Design

## Environment Summary


## Log Sources


## Collection + Transport Plan


## Normalization Plan


## Retention and Access Plan

# Day 11 — Log Centralization Architecture Design

## The Company

Fictional mid-size company. 65 endpoints total:
- 50 Windows workstations
- 10 Linux servers
- 5 network devices (routers, firewalls, switches)
- 1 cloud environment (AWS)

---

## Question 1 — What log sources exist and what 
format does each use?

| Source | Count | Log format | Notes |
|---|---|---|---|
| Windows workstations | 50 | Windows Event Log (XML) | Event IDs like 4624, 4625, 4688 |
| Linux servers | 10 | Syslog / journald | RFC 5424 format ideally |
| Network devices | 5 | Syslog (vendor-specific) | Format varies by vendor |
| AWS cloud | 1 | CloudTrail JSON | Structured but needs API to collect |

Four sources, four completely different formats. 
None of them speak the same language out of the box.

---

## Question 2 — How do you collect from each one?

**Windows workstations (50 machines)**

Windows doesn't speak syslog. You need an agent on 
every machine. The options:

- **Winlogbeat** (free, Elastic ecosystem) — reads 
  Windows Event Log and forwards as JSON
- **NXLog** (free community edition) — more flexible, 
  can forward to multiple destinations
- **Windows Event Forwarding (WEF)** — built into 
  Windows, no agent needed, but requires a Windows 
  collector server

For 50 machines I'd use Winlogbeat. It's free, it 
integrates directly with Elastic/Wazuh, and one 
config file deployed across all machines handles 
everything.

**Linux servers (10 servers)**

rsyslog is already running on most Linux systems. 
Just configure it to forward to a central collector:
Add to /etc/rsyslog.conf on each server
. @@10.0.0.100:514   # TCP forwarding to collector

No extra software needed. Already built in.

**Network devices (5 devices)**

Routers, firewalls, and switches all speak syslog 
but the field names and formats vary by vendor. 
A Cisco router formats things differently from a 
pfSense firewall.

Configure each device to send syslog to your 
collector IP on UDP port 514. Then normalize the 
vendor-specific fields at ingestion.

Most network devices only support UDP syslog — 
no acknowledgment, no guarantee of delivery. 
If the collector is down, those logs are gone. 
Something to plan for.

**AWS cloud (1 environment)**

AWS doesn't push logs to you. You have to pull them.

- Enable **CloudTrail** for API activity logs
- Enable **VPC Flow Logs** for network traffic
- Use **CloudWatch Logs** for application logs
- Pull via AWS API or use a native integration

Most SIEMs have an AWS integration that polls 
CloudTrail every few minutes. The delay means 
cloud alerts are slightly behind real-time 
compared to on-premises sources.

---

## Question 3 — How do you normalize everything?

Every source uses different timestamp formats, 
field names, and structures. Without normalization 
you can't correlate events across sources.

| Source | Timestamp format | Problem | Fix |
|---|---|---|---|
| Windows | 2026-05-20T12:11:09Z (UTC) | None — already UTC ISO 8601 | Map field names to common schema |
| Linux rsyslog | 2026-05-24T18:07:58+01:00 | Timezone offset varies per server | Convert to UTC at ingestion |
| Network devices | Vendor-specific, often no year | Format inconsistent, may be local time | Parse per-vendor, add year, convert to UTC |
| AWS CloudTrail | ISO 8601 UTC | None — already clean | Map action fields to common schema |

Common schema fields every normalized event should have:
- `timestamp_utc` — always UTC
- `source_host` — which machine
- `source_type` — windows/linux/network/cloud
- `action` — what happened
- `user` — who did it
- `severity` — how important

Without this every search query would have to 
account for different field names across sources. 
In a real incident you don't have time for that.

---

## Question 4 — What SIEM would you choose and why?

For this company size I'd go with **Wazuh + Elastic**.

**Why Wazuh:**
- Free and open source — no licensing cost
- Built-in agents for Windows and Linux
- Native syslog receiver for network devices
- Has its own normalization rules built in
- Scales to 65 endpoints easily

**Why Elastic alongside it:**
- Wazuh integrates directly with Elastic Stack
- Kibana gives you dashboards and search
- Elasticsearch handles the indexing and retention
- All still free at this scale

**What I'd avoid for this company:**
- Splunk — too expensive for a 65-endpoint company. 
  Pricing is per GB of data ingested and it adds 
  up fast.
- Microsoft Sentinel — good if you're already 
  all-in on Azure. This fictional company uses AWS 
  so Sentinel would add unnecessary complexity.

**The real trade-off:**
Wazuh + Elastic requires someone who knows how to 
maintain it. There's no vendor support unless you 
pay for it. For a company with dedicated IT staff 
that's fine. For a 5-person company with no IT 
department, Sentinel or a managed SIEM service 
would be better even if it costs more.

---

## Architecture Flow
Windows machines (50)
└── Winlogbeat agent →
Linux servers (10)
└── rsyslog forward →
Network devices (5)          → Central Collector → Wazuh → Elastic → Kibana
└── UDP syslog 514 →                               ↓
Alerts &
AWS CloudTrail                                     Dashboards
└── API poll →

---

## What I'd Do on Day 1 as the Analyst

Before touching any SIEM config:
1. Inventory every log source — you can't collect 
   what you don't know about
2. Check which sources are already sending logs 
   somewhere — avoid duplicate ingestion
3. Confirm timestamps are in UTC or have timezone 
   info — silent timezone bugs destroy correlation
4. Set up collection for the highest-value sources 
   first: Windows 4624/4625/4688, Linux sudo/auth, 
   firewall deny logs

The SIEM comes last. Getting the pipeline right 
comes first.
