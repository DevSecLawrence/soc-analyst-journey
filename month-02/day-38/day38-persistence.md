# Day 38 — Windows Persistence Mechanisms

I studied how attackers stay on a Windows host after reboot. I mapped the common persistence spots, compared them to normal admin activity, and wrote detections for the abuse patterns that matter.

The local Windows VM was down, so I did not pretend that was fine. I used ATT&CK, Autoruns docs, and browser-lab telemetry to stay honest and keep the analysis moving.

## What I Did
- Reviewed MITRE ATT&CK persistence tactic TA0003
- Mapped registry Run keys, scheduled tasks, services, WMI subscriptions, and startup folder entries
- Baseline normal admin and software behavior against attacker behavior
- Wrote Sigma rules for the five main persistence paths

## What Stood Out
- Registry Run keys are noisy but still useful because they are common
- Scheduled tasks blend in when the name looks normal
- Services are high value because they run with real privilege
- WMI subscriptions are easy to miss if you do not look for them on purpose
- Startup folder abuse is simple and still works

## Files
- [day38-persistence-baseline.md](./day38-persistence-baseline.md) — normal vs suspicious persistence locations
- [day38-persistence-detections/](./day38-persistence-detections/) — Sigma rules for the five persistence types

## What I Concluded
Persistence is not just a malware trick. It is a trail. If I can see where an attacker tried to survive a reboot, I can usually tell what kind of access they wanted and how much effort they spent hiding it.

## Assumption I Made
I assumed browser-lab telemetry was enough to model the detection logic even though my local Windows VM was down.

## Uncertainty I Have
I do not know yet which persistence mechanism should be hunted first in a real enterprise, because that depends on the environment and the telemetry I actually have.