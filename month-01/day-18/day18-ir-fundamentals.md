# Day 18 — IR Fundamentals (IR Lifecycle)

I used NIST 800-61 Section 3 to map the IR lifecycle to what a SOC analyst actually does.

## Medium Exercise Answers (NIST 800-61 Section 3)

### Preparation
- SOC analyst role: Make sure logging, alerting, and baseline visibility are in place before incidents hit.
- Escalation decisions: Gaps in telemetry, missing coverage, or lack of IR tooling go to senior staff.
- Artifacts to preserve: Baselines, asset inventory, network diagrams, escalation lists.

### Detection & Analysis
- SOC analyst role: Triage alerts, validate if it is an incident, scope affected users/systems.
- Escalation decisions: Severity, business impact, suspected data loss, or external exposure.
- Artifacts to preserve: Raw logs, alert metadata, timelines, affected host/user list.

### Containment, Eradication, Recovery
- SOC analyst role: Execute containment steps, coordinate with IR/IT for eradication and recovery.
- Escalation decisions: When containment impacts business operations or requires legal/PR input.
- Artifacts to preserve: Forensic images, mailbox exports, file hashes, system snapshots.

### Post-Incident Activity
- SOC analyst role: Document lessons learned, detection gaps, and fixes.
- Escalation decisions: Policy changes, training needs, and budget/resource asks.
- Artifacts to preserve: Final report, lessons learned notes, updated playbook version.

## What I Concluded
- The phase that surprised me most was Post-Incident 
Activity. I expected it to be a recap — close the 
ticket, move on. NIST treats it as the phase that 
actually improves the whole process. The lessons 
learned meeting isn't a debrief, it's supposed to 
produce documented agreement and action items: 
what happened, what worked, what failed, what 
needs to change, and what to watch for next time. 
Without that output, every incident is an isolated 
event. With it, each incident makes the team 
better at handling the next one.

The other thing that genuinely changed how I think 
was the containment strategy section. I assumed 
containment was straightforward — isolate fast, 
ask questions later. NIST pushes back on that. 
There are six decision criteria: damage potential, 
evidence needs, service impact, time and resources, 
effectiveness, and duration. "Always pull the plug" 
isn't a containment strategy. It's a panic response. 
A real containment decision balances all six factors 
and sometimes that means monitoring a threat longer 
rather than triggering it to hide or escalate.

The evidence section reinforced something from 
Day 16 — documentation of who handled evidence, 
when, and where it's stored matters as much as 
the evidence itself. Chain of custody isn't 
bureaucracy. It's what makes evidence usable 
in legal proceedings and what proves the 
investigation was conducted properly.

## Assumption I Made
- 

## Uncertainty I Have
- 
