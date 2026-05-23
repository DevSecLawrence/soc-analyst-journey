# Day 10 — Linux auditd: Seeing What the OS Sees

## Medium Exercise — Logging Commands with auditd

### Setup

Installed and started auditd on Kali:
sudo apt install auditd -y
sudo systemctl start auditd

Then added the execve rules to catch every command execution:
sudo auditctl -a always,exit -F arch=b64 -S execve -k commands
sudo auditctl -a always,exit -F arch=b32 -S execve -k commands

Both rules needed — b64 catches 64-bit processes, b32 catches 
32-bit. Missing either one means gaps in your coverage.

---

### Running the 5 Recon Commands
whoami
id
hostname
uname -a
ls /etc

These are the Linux version of what I did on Day 9 with 
Windows. Same intent — figure out who you are, what machine 
you're on, and what's available.

The `id` output on my machine was particularly interesting:
uid=1000(lawrence) gid=1000(lawrence)
groups=1000(lawrence),4(adm),20(dialout),24(cdrom),
25(floppy),27(sudo),29(audio),44(video),124(wireshark)...

I'm in the sudo group. On a compromised machine, that's the 
first thing an attacker checks — `id` tells them immediately 
whether they can escalate without any further exploitation. 
One command, full privilege picture.

The `ls /etc` output on Kali was massive. Tools like 
`theHarvester`, `netsniff-ng`, `proxychains4`, `nikto`, 
`powershell-empire` all have config files there. An attacker 
listing /etc on a Kali machine knows they're on a pentest 
box — that context changes everything about how they operate.

---

### Reading the Audit Log
sudo ausearch -k commands --start today

One audit entry is actually three linked records:

**PROCTITLE** — the encoded process title. The hex string 
at the top is the command name in hex. Not human readable 
directly but it's there.

**EXECVE** — the actual command and its arguments. This is 
the field that matters most:
type=EXECVE argc=2 a0="/bin/sh"
a1="/usr/share/kali-themes/xfce4-panel-genmon-vpnip.sh"

**SYSCALL** — the low-level call details. exe="/usr/bin/dash" 
tells you exactly which binary ran. The auid field (audit 
user ID) tracks back to the original logged-in user even 
if they switched to another account.

**CWD** — current working directory when the command ran:
cwd="/home/lawrence"

Together these three records answer: what ran, with what 
arguments, by whom, and from where. That's more context 
than a single Windows event gives you.

---

## Hard Exercise — Sensitive File and Tool Monitoring

### Rules Added

After running `auditctl -D` to clear existing rules, I added 
5 new rules using modern syntax:
sudo auditctl -a always,exit -F path=/etc/passwd -F perm=wa -k passwd_changes
sudo auditctl -a always,exit -F path=/etc/shadow -F perm=wa -k shadow_changes
sudo auditctl -a always,exit -F path=/usr/bin/sudo -F perm=x -k sudo_usage
sudo auditctl -a always,exit -F path=/usr/bin/curl -F perm=x -k network_tools
sudo auditctl -a always,exit -F path=/usr/bin/wget -F perm=x -k network_tools

Confirmed with `auditctl -l` — all 5 rules showing.

Note: the rules file shows them in the old -w format because 
auditctl -l displays them that way regardless of how you 
added them. The underlying behaviour is the same.

---

### What Each Rule Detects and Why It Matters

**passwd_changes and shadow_changes**

/etc/passwd and /etc/shadow are the two most important files 
on a Linux system from an attacker's perspective. /etc/passwd 
holds user account info. /etc/shadow holds password hashes.

Monitoring writes to these files catches:
- An attacker adding a backdoor account
- Privilege escalation by modifying UID to 0
- Password hash extraction preparation

I tested with `sudo cat /etc/passwd` — the rule fires on 
any access involving those files through sudo, creating a 
trail even for read operations.

**sudo_usage**

Every time sudo is called this rule fires. In a normal 
environment sudo is used constantly by admins. But 
unexpected sudo usage from accounts that shouldn't have 
it, at unusual times, or running unusual commands — that's 
your alert.

**network_tools**

curl and wget are how attackers download payloads and 
exfiltrate data. These tools are completely legitimate 
in normal use but their execution from unexpected 
directories, by unexpected users, or at unexpected 
times is a post-exploitation signal.

Testing with:
curl http://example.com -s -o /dev/null
sudo ausearch -k network_tools --start today

The audit trail showed exactly which user ran curl, 
from which directory, and at what time.

---

### The Old Style Warning

When I first used `-w` syntax auditd warned me:
Old style watch rules are slower

The modern `-F path=` syntax is faster because it uses 
the kernel's inode-based matching instead of pathname 
lookups. On a busy server with thousands of file 
operations per second, that performance difference 
matters. I cleared the old rules with `auditctl -D` 
and rewrote them in modern syntax.

This is the kind of detail that doesn't show up in 
tutorials but matters in a production environment — 
the difference between a rule that keeps up with 
real traffic and one that creates a bottleneck.

---

### auditd vs Windows 4688

Comparing today to Day 9:

| | Linux auditd | Windows 4688 |
|---|---|---|
| Default state | Needs manual setup | Exists but cmdline blank by default |
| Record structure | 3 linked records per event | 1 event with all fields |
| User tracking | auid persists across su/sudo | SubjectUserName |
| File monitoring | Built into auditd rules | Needs separate Sysmon config |
| Persistence | Rules lost on reboot unless saved | Persists automatically |

The auditd persistence issue is a real gap — rules I added 
today with auditctl -a are gone after a reboot. To make 
them permanent they need to go into /etc/audit/rules.d/. 
For this lab I saved them to a file instead. In a real 
deployment that would be unacceptable — a server reboot 
would silently remove all detection capability.

---

## What I Concluded

The biggest thing today was realising auditd splits every 
event across multiple record types linked by timestamp. 
That structure makes sense once you understand it — SYSCALL 
tells you what happened at the kernel level, EXECVE tells 
you what was actually run, CWD tells you where it ran from. 
But until you see it the first time it looks like noise.

The sensitive file monitoring rules are genuinely useful. 
The /etc/passwd and /etc/shadow rules in particular — any 
write to those files on a production machine is worth 
investigating immediately. There's almost no legitimate 
reason for automated processes to be modifying those files.

## Assumption I Made

I assumed rules added with `auditctl -a` would persist 
across sessions. They don't. Every rule I added today 
is gone the moment auditd restarts or the machine 
reboots. That's a significant operational gap. In a 
real SOC deployment you'd write rules to 
/etc/audit/rules.d/audit.rules and use augenrules 
to load them permanently. I didn't do that today — 
something to fix before relying on this in a real 
environment.

## Uncertainty I Have

The aureport output gives summaries but I haven't dug 
into how to use it for timeline reconstruction during 
an actual investigation. If I have a timestamp of when 
something suspicious happened, can aureport help me 
build a full activity picture around that moment? That's 
what I want to test next. The raw ausearch output is 
comprehensive but hard to read at scale — I want to 
understand when aureport is the right tool vs ausearch.