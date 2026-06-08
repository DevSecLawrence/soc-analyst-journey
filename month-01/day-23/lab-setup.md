# Day 23 — Building the Detection Lab: Virtualization Basics

**Date:** 2026-06-06
**Environment:** Windows Host + VirtualBox + Kali VM (existing) + Windows 10 VM (new)

---

## Goal

Set up an isolated two-VM detection lab:
- **Windows 10 VM** — the target machine (where attacks happen)
- **Kali Linux VM** — the monitoring and analysis side

Both VMs on a host-only network — no internet access on the Windows side. The whole point is that nothing that happens in this lab touches the real network.

---

## My Setup Before Starting

- Host machine: Windows (16GB RAM)
- VirtualBox already installed (Kali was already running)
- Windows 10 ISO: official Microsoft eval ISO (Windows 10 19H2, 64-bit)
- Storage situation: less than 30GB free on C: — ISO and VM stored on external drive (D:)

---

## What I Did

### Step 1 — Created the Windows 10 VM

Opened VirtualBox → New. Named it `Win10-DetectionLab`.

Key settings I used:
- **Machine folder:** pointed to external drive (D:\VMs) — not C: because I didn't have the space
- **RAM:** 4096 MB
- **Hard disk:** VDI, dynamically allocated, 40GB — also saved to external drive
- **ISO:** attached directly from external drive, no copying

One thing I ran into — VirtualBox's unattended install setup tried to auto-fill a product key and flagged an error because the eval ISO doesn't use one. Fixed it by clearing the product key field and unchecking "Install in Background" so I could click through the setup manually.

Also left the domain name as `myguest.virtualbox.org` — VirtualBox flags an error if you clear it, and it doesn't actually try to join any domain so it doesn't matter.

### Step 2 — Installed Windows 10

Booted the VM from the ISO. Clicked through the installer manually:
- No product key → "I don't have a product key"
- Selected **Windows 10 Pro**
- Custom install → selected the virtual disk
- Install took about 15–20 minutes
- Account setup: used local account, username `lawrence`

### Step 3 — Installed Guest Additions

After getting to the desktop, installed VirtualBox Guest Additions so I could use shared clipboard and shared folders between the host and VM:

VirtualBox menu → Devices → Insert Guest Additions CD image → ran `VBoxWindowsAdditions.exe` inside the VM → rebooted.

This was important because the Windows VM has no internet — the only way to get files into it is through shared folders from the host.

### Step 4 — Network Configuration

**The decision:** Host-only for Windows VM, dual adapter for Kali.

- **Windows 10 VM:** Adapter 1 → Host-only Adapter → `vboxnet0` (no internet — intentional)
- **Kali VM:** Adapter 1 → Bridged (keeps internet for tools/updates), Adapter 2 → Host-only → `vboxnet0` (can talk to Windows VM)

This way Kali keeps full internet access for `apt` and tool downloads, but can still communicate with the Windows VM on the internal network. The Windows VM stays completely isolated.

**Verified isolation:**
- Inside Windows VM → `ping 8.8.8.8` → failed ✅ (no internet, as expected)
- Inside Kali → ping to Windows VM IP → took time due to Windows Firewall blocking ICMP by default (not a real connectivity issue — just Windows blocking pings)

### Step 5 — Setback

Hit a storage issue during the lab setup — accidentally formatted the external drive that had the VM and ISO on it. Lost the Windows 10 VM and ISO.

Lab setup is paused. Will re-download the ISO and rebuild the VM when storage is recovered. Everything up to the network configuration was confirmed working before the setback.

Sysmon install and auditd configuration will be completed on Day 23 (continued) once the lab is back up.

---

## What I Learned

Building a lab sounds straightforward until you're actually doing it. The network isolation piece is the thing that matters most — it's not just a checkbox, it's the entire safety model for everything that comes after this. Running attack simulations on a VM with internet access is exactly the kind of mistake that makes a real incident.

The dual adapter setup for Kali (bridged for internet + host-only for lab traffic) was something I hadn't thought about before. Switching Kali fully to host-only would have broken all my tool updates and downloads. Keeping Adapter 1 as bridged and adding a second host-only adapter solved that cleanly.

The storage situation also taught me something practical — always check where VirtualBox is saving VM files before creating them. The default is always C: and that'll fill up fast once you start spinning up multiple VMs.

---

## What's Left (Day 23 Continued)

- [ ] Re-download Windows 10 eval ISO
- [ ] Rebuild Win10-DetectionLab VM
- [ ] Install Sysmon with SwiftOnSecurity config
- [ ] Verify auditd on Kali
- [ ] End-to-end test — trigger a process on Windows, confirm Sysmon logs it

---

## Assumption I Made

I assumed the ping test between VMs was the right way to verify network connectivity. It's not reliable when Windows Firewall is running because it blocks ICMP by default. The real connectivity test is whether Sysmon logs can be pulled from Windows into a SIEM or whether Kali can reach an open port on the Windows VM — not just ping.

---

## Uncertainty I Have

I don't know yet whether the host-only network will assign consistent IPs to both VMs every time they boot or whether the DHCP will give them different IPs each session. If the IPs change every boot that'll be a problem when I start configuring log forwarding from Windows to Kali in the coming days. I need to look into setting static IPs for both VMs on the host-only adapter.