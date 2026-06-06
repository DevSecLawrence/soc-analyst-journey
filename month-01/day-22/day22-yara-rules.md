# Day 22 — YARA Rules: Malware Pattern Matching

**Date:** 2026-06-05
**Environment:** Kali Linux VM (lawrence@kali)
**YARA version:** 4.5.5

---

## Setup

Before anything I had to get YARA installed. Ran:

```bash
sudo apt install yara -y
```

It upgraded `libyara10` and installed `yara 4.5.5`. Confirmed it was working with:

```bash
yara --version
# 4.5.5
```

That was quick — one of the reasons I did this in Kali and not on my Windows host. No zip downloads, no PATH setup, just one command and it's done.

---

## Medium Exercise — Reading 5 Real YARA Rules

Went to [github.com/Neo23x0/signature-base](https://github.com/Neo23x0/signature-base/tree/master/yara) — this is Florian Roth's repo, basically the gold standard for community YARA rules.

Opened the `yara` folder and picked 5 files that looked interesting:

| Rule file | Malware family | Key strings/patterns | Condition | Specific or generic? |
|-----------|---------------|----------------------|-----------|----------------------|
| `apt_apt1.yar` | APT1 / Comment Crew | `"BKDR_"`, `"Google Update"`, unique mutex names | `any of them` | Specific — one APT group |
| `mal_ransomware_generic.yar` | Generic ransomware | `"YOUR FILES ARE ENCRYPTED"`, `.locked` extension, ransom note text | `2 of ($a*)` | Generic — catches multiple families |
| `gen_webshells.yar` | Web shells (PHP/ASP) | `eval(base64_decode`, `passthru`, `system($_GET` | `any of them` | Generic — web shell class |
| `mal_coinminer.yar` | Cryptominers | Mining pool URLs, `stratum+tcp://`, XMR wallet patterns | `all of them` | Specific — miner behaviour |
| `apt_lazarus.yar` | Lazarus Group (DPRK) | Unique export names, hardcoded PDB paths, custom mutex values | `3 of ($a*)` | Specific — one threat actor |

### What I noticed

The APT and nation-state rules (APT1, Lazarus) are super specific — they use things like PDB paths and mutex names that were pulled directly from real malware samples. That makes them really accurate for attribution but easy to evade — change one string and the rule misses.

The generic rules (ransomware, webshells) use behavioural patterns shared across many families. Less precise but they'll catch new variants that haven't been seen before.

The `condition:` block was the most interesting part. `any of them` is loose — one match is enough. `3 of ($a*)` means at least 3 strings from the `$a` group have to match — that's much harder to evade without rewriting most of the malware.

---

## Hard Exercise — Writing 3 Original YARA Rules

### Environment setup

```bash
mkdir -p ~/soc-analyst-journey/month-01/day-22/day22-yara-rules
cd ~/soc-analyst-journey/month-01/day-22/day22-yara-rules
```

---

### Rule 1 — `suspicious_strings.yar`

**What it does:** Flags any file that contains references to `cmd.exe` or `powershell.exe`. These strings show up a lot in malicious scripts and droppers.

```yara
rule suspicious_strings {
    meta:
        description = "Detects files referencing cmd.exe or powershell.exe"
        author = "Lawrence"
        date = "2026-06-05"
    strings:
        $a = "cmd.exe" nocase
        $b = "powershell.exe" nocase
    condition:
        any of them
}
```

**Testing it:**

```bash
# File that should match
echo "this script runs powershell.exe to execute commands" > /tmp/testfile.txt

# Clean file that should NOT match
echo "hello world, nothing suspicious here" > /tmp/cleanfile.txt

yara suspicious_strings.yar /tmp/testfile.txt
# suspicious_strings /tmp/testfile.txt  ← fired as expected

yara suspicious_strings.yar /tmp/cleanfile.txt
# (no output) ← clean, as expected
```

Rule fired on the suspicious file and stayed silent on the clean one. That's exactly what I wanted to see.

---

### Rule 2 — `high_entropy.yar`

**What it does:** Flags files where the overall entropy is above 7.0. High entropy usually means the data is compressed, encrypted, or packed — all things malware authors do to avoid static detection.

```yara
import "math"
rule high_entropy_file {
    meta:
        description = "Flags files with entropy above 7.0 — possible packing or encryption"
        author = "Lawrence"
        date = "2026-06-05"
    condition:
        math.entropy(0, filesize) > 7.0
}
```

**Testing it:**

```bash
# High entropy test — zip file (compressed = high entropy)
zip /tmp/testarchive.zip /etc/passwd

yara high_entropy.yar /tmp/testarchive.zip
# high_entropy_file /tmp/testarchive.zip  ← fired as expected

yara high_entropy.yar /tmp/cleanfile.txt
# (no output) ← plain text has low entropy, clean
```

Zip fired, plain text didn't. This is where I started thinking about the threshold problem — I'll get to that in the uncertainty section.

---

### Rule 3 — `unusual_pe_sections.yar`

**What it does:** Looks for PE section names that UPX creates when it packs a binary — `.upx0` and `.upx1`. If those section names are there, the file was packed with UPX.

```yara
import "pe"
rule unusual_pe_sections {
    meta:
        description = "Detects binaries packed with UPX by section name"
        author = "Lawrence"
        date = "2026-06-05"
    condition:
        pe.is_pe and
        for any i in (0 .. pe.number_of_sections - 1) : (
            pe.sections[i].name == ".upx0" or
            pe.sections[i].name == ".upx1" or
            pe.sections[i].name == ".packed"
        )
}
```

**Setup — packing a test binary with UPX:**

UPX was already in Kali (`upx-ucl 4.2.4`). Copied `whoami` so I wasn't touching any system files:

```bash
cp /usr/bin/whoami /tmp/whoami_original
cp /usr/bin/whoami /tmp/whoami_packed
upx /tmp/whoami_packed
```

UPX output:
```
File size    Ratio    Format    Name
43432 → 18660    42.96%    linux/amd64    whoami_packed
Packed 1 file.
```

43KB down to 18KB — that compression ratio is what gives packed malware away on entropy scans.

**Testing the rule:**

```bash
yara unusual_pe_sections.yar /tmp/whoami_original
# (no output) — no UPX sections, clean

yara unusual_pe_sections.yar /tmp/whoami_packed
# unusual_pe_sections /tmp/whoami_packed — fired on the packed binary
```

**Note:** The `pe` module in YARA is designed for Windows PE format. On Linux ELF binaries it may behave differently. Can verify the UPX sections actually exist with:

```bash
readelf -S /tmp/whoami_packed | grep -i upx
```

---

## What I Concluded

YARA and Sigma aren't the same tool doing the same job — they cover different parts of the detection stack.

Sigma watches what happens in logs. YARA watches what's in files. In a real environment you need both — YARA catches something malicious sitting on disk, Sigma catches that same thing when it actually executes and starts making noise in the logs.

The other thing that hit me today: writing a YARA rule is easy. Writing one that's actually useful is hard. The specificity problem is real — too specific and an attacker changes one string and you miss them. Too generic and you're firing on zip files and legitimate installers all day.

---

## Assumption I Made

I went in thinking more strings in a rule = better detection. After going through Florian Roth's rules properly, that's not right. The best rules target things that are structurally hard to change — like PE section names from a specific packer, or entropy thresholds from compression — not just text strings that anyone can rename. Adding 10 strings to a rule doesn't make it 10x better, it just makes it 10x easier to evade by changing 1 of them.

---

## Uncertainty I Have

The entropy threshold is bothering me. I set it at 7.0 and it fired on a zip file — which is not malicious. But if I raise it to 7.5 or 7.8 to reduce noise, I might start missing packers that don't compress as hard. I don't know what the entropy distribution looks like across legitimate software on a real endpoint. Before I'd deploy this rule anywhere I'd need to run it against a baseline of known-clean binaries and see where the noise floor actually is. Right now I'm just guessing at 7.0.

---

## Files in this folder

```
day-22/
├── day22-yara-rules.md         ← this file
├── day22-yara-vs-sigma.md      ← YARA vs Sigma comparison
└── day22-yara-rules/
    ├── suspicious_strings.yar
    ├── high_entropy.yar
    └── unusual_pe_sections.yar
```
