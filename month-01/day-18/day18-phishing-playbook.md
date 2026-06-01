# Day 18 — Phishing to Credential Theft Playbook

## Detection Criteria
- User reports a suspicious email with a login link.
- SIEM alert on known phishing domain or suspicious URL.
- EDR or email security flags credential theft indicators.

## Initial Triage
- Pull the email headers and URL.
- Identify impacted user(s).
- Check if the user clicked or submitted creds.
- Review sign-in logs for unusual activity.

## Containment Actions
- Reset affected user passwords and revoke sessions.
- Block sender domain and malicious URL in email gateway.
- Quarantine the email across mailboxes.

## Escalation Criteria
- Multiple users impacted.
- Confirmed credential submission.
- Signs of lateral movement or mailbox access.

## Evidence Preservation
- Save the original email and headers.
- Export mailbox (if required).
- Preserve sign-in logs and alert artifacts.

## Recovery Steps
- Verify account access is restored securely.
- Monitor for re-compromise attempts.
- Close gaps in email filtering rules.


