# Day 29 — BTLO Network Analysis: Web Shell Investigation

**Date:** 2026-06-11
**Platform:** Blue Team Labs Online
**Challenge:** Network Analysis — Web Shell
**Difficulty:** Easy
**Tool used:** Wireshark (Kali VM)

---

## Scenario

The SOC received an alert for "Local to Local Port Scanning" — an internal IP began scanning another internal system. Investigate the PCAP and determine whether the activity is malicious.

---

## Initial Hypothesis

Before opening the PCAP — port scanning between two internal IPs usually means either an authorised vulnerability scan or early-stage reconnaissance from a compromised internal host. Given this is a SOC alert and not a routine scan, my guess going in was this was the early stage of an internal attacker (or compromised machine) probing for open services to exploit.

---

## Investigation

### Step 1 — Identify the Scanning IP

Opened the PCAP in Wireshark → Statistics → Conversations → TCP tab. Sorted by Port B to spot the pattern.

**Finding:** `10.251.96.4` was sending traffic to nearly every port on `10.251.96.5` — classic port scan signature, one IP hitting a wide range of ports on a single target.

### Step 2 — Confirm the Port Range

Sorted Port B ascending and descending in the Conversations window.

**Finding:** Ports 1–1024 scanned — the well-known port range. This points to a generic recon scan rather than a targeted scan against one specific service.

### Step 3 — Web Directory Brute Force

Filtered by `http` and looked through the request list. Found a burst of rapid GET requests to different paths on the web server, mostly returning 404s — the signature of a directory brute force tool.

Checked the User-Agent header on one of the requests to identify the tool used for the brute force.

### Step 4 — Web Shell Upload

Filtered by `http.request.method == POST`. Found a POST request and followed the TCP stream.

**Finding:** The attacker uploaded a file called `dbfunctions.php` — this is the web shell. Reading the uploaded PHP code, the parameter used to execute commands through the shell is `cmd`.

### Step 5 — Commands Executed

Filtered by `ip.src == 10.251.96.4 && http.request.method == GET` to see the GET requests hitting the web shell with the `cmd` parameter.

**Findings — three commands run in order:**
1. `id`
2. `whoami`
3. A Python one-liner establishing a reverse shell

### Step 6 — Reverse Shell

Followed the TCP stream on the third GET request. The Python command connects back to the attacker's IP on a specific port and spawns `/bin/sh`.

**Finding:** Reverse shell connects back on port `4422`.

---

## Attack Chain

```
Port scan (10.251.96.4 → 10.251.96.5, ports 1-1024)
        ↓
Directory brute force (gobuster)
        ↓
Web shell upload via POST (dbfunctions.php)
        ↓
Command execution via GET (id, whoami)
        ↓
Reverse shell established (Python → port 4422)
```

---

## What I Concluded

This was a textbook web application compromise from initial recon all the way to a reverse shell — and it's all visible in a single PCAP if you know what to filter for. The pattern matters more than any single packet: port scan → directory enumeration → file upload → command execution → shell. Recognising that chain is more valuable than memorising any one step in isolation.

The web shell itself was almost laughably simple — one parameter (`cmd`) handling arbitrary command execution. That's the entire vulnerability. No exotic exploit, just an upload function that didn't validate what was being uploaded.

---

## Hypothesis Evolution

Started thinking: compromised internal host doing recon.

Actual attack: external-style web application attack chain happening over what looked like an internal scan — port scan against a web server, followed by brute forcing directories to find an upload point, followed by uploading a PHP web shell, followed by using that shell to get a full reverse shell. The "local to local" framing in the alert made me initially assume insider-style lateral movement. It was actually a complete external attack chain against a web app that just happened to be on an internal network segment.

---

## Assumption I Made

I assumed "local to local" meant insider threat or lateral movement from an already-compromised machine. It didn't — it just meant the attacker's scanning machine and the target web server were both on the internal network, which could mean the attacker already had a foothold elsewhere, or the web server was reachable from inside without proper segmentation. The alert label describes where the traffic originated, not the nature of the attacker.

---

## Uncertainty I Have

I don't know how the attacker got onto the internal network in the first place to run this scan. The PCAP only shows what happened starting from the port scan — it doesn't show initial access to the network itself. In a real investigation I'd need additional log sources (VPN logs, firewall logs, other endpoint telemetry) to answer that question. A single PCAP gives you one slice of the attack, not the whole story.
