# Day 17 — URL + Attachment Triage Summary

This ties together the URL triage and the document sandbox analysis from today.

## Summary
- What I saw across the 5 URLs: I finished two cases end-to-end. One was dead (404) but still flagged by VT, and the other redirected to a legit Epic Games login page. The other three cases still need VT + URLScan screenshots.
- What the sandboxed document did: I loaded a MalwareBazaar docx sample in Any.run and saw the basic run results, but I still need the Network/Files/Registry/Processes tabs to pull the real IOCs.
- What I would block: The suspicious source URL and any repeating pattern from the dead phish domain once I finish the remaining cases.
- What I would alert on: URL redirects from unknown domains to branded login pages, plus repeated hits to those same short-lived domains.
- What I would tell the user: Don’t click or log in through links in unexpected messages, and report any link that forces a login screen.

## Lessons Learned
- VT detections can be low even when the URL is still a problem.
- Redirect chains matter; the first hop can be bad even if the final URL is legit.
- I need the full Any.run tab captures to make the attachment analysis complete.

## Evidence
- Links:
  - [day17-url-analysis.md](./day17-url-analysis.md)
  - [day17-malware-triage.md](./day17-malware-triage.md)
