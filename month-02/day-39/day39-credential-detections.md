**Date:** 2026-07-07
**Note:** Rules written from research — not yet tested against live telemetry (lab pending). Will validate when Windows VM is rebuilt.
 
---
 
## Detection 1 — LSASS Access by Unexpected Process
 
**Technique:** T1003.001 — LSASS Memory Dumping
**Log source:** Sysmon Event ID 10
 
```yaml
title: Suspicious LSASS Process Access
id: d39-001
status: experimental
description: Detects unexpected processes accessing LSASS memory — common in credential dumping tools like Mimikatz
references:
    - https://attack.mitre.org/techniques/T1003/001/
author: Lawrence
date: 2026-07-07
tags:
    - attack.credential_access
    - attack.t1003.001
logsource:
    product: windows
    category: process_access
detection:
    selection:
        TargetImage|endswith: '\lsass.exe'
        GrantedAccess|contains:
            - '0x1010'
            - '0x1410'
            - '0x1438'
            - '0x143a'
    filter_legitimate:
        SourceImage|contains:
            - '\Windows\System32\svchost.exe'
            - '\Windows\System32\wininit.exe'
            - '\Windows\System32\csrss.exe'
            - '\Windows\System32\services.exe'
            - '\Windows\System32\lsm.exe'
            - '\Windows\System32\taskmgr.exe'
    condition: selection and not filter_legitimate
falsepositives:
    - Security products that monitor LSASS legitimately
    - Some EDR agents access LSASS as part of normal operation
level: high
```
 
---
 
## Detection 2 — VSS Shadow Copy Access for SAM Extraction
 
**Technique:** T1003.002 — SAM Database
**Log source:** Sysmon Event ID 1
 
```yaml
title: SAM Database Access via Volume Shadow Copy
id: d39-002
status: experimental
description: Detects attempts to access SAM database through volume shadow copies — a common technique for offline credential extraction
references:
    - https://attack.mitre.org/techniques/T1003/002/
author: Lawrence
date: 2026-07-07
tags:
    - attack.credential_access
    - attack.t1003.002
logsource:
    product: windows
    category: process_creation
detection:
    vssadmin:
        Image|endswith: '\vssadmin.exe'
        CommandLine|contains: 'shadow'
    reg_save:
        Image|endswith: '\reg.exe'
        CommandLine|contains:
            - 'save'
            - 'HKLM\SAM'
    condition: vssadmin or reg_save
falsepositives:
    - Legitimate backup software using vssadmin
    - IT admin scripts backing up registry
level: high
```
 
---
 
## Detection 3 — Kerberoasting via Unusual Service Ticket Requests
 
**Technique:** T1558.003 — Kerberoasting
**Log source:** Windows Security Event ID 4769
 
```yaml
title: Kerberoasting — Suspicious Service Ticket Request
id: d39-003
status: experimental
description: Detects Kerberoasting attempts via RC4 encrypted service ticket requests — attackers request tickets to crack offline
references:
    - https://attack.mitre.org/techniques/T1558/003/
author: Lawrence
date: 2026-07-07
tags:
    - attack.credential_access
    - attack.t1558.003
logsource:
    product: windows
    service: security
detection:
    selection:
        EventID: 4769
        TicketEncryptionType: '0x17'
        ServiceName|not endswith: '$'
    filter_legitimate:
        ServiceName:
            - 'krbtgt'
    condition: selection and not filter_legitimate
falsepositives:
    - Legacy applications that only support RC4 encryption
    - Older Windows systems that haven't been updated to support AES
level: medium
```
 
---
 
## Detection 4 — Browser Credential File Access
 
**Technique:** T1555.003 — Credentials from Web Browsers
**Log source:** Sysmon Event ID 11
```yaml
title: Suspicious Access to Browser Credential Store
id: d39-004
status: experimental
description: Detects unexpected processes accessing browser saved password databases
references:
    - https://attack.mitre.org/techniques/T1555/003/
author: Lawrence
date: 2026-07-07
tags:
    - attack.credential_access
    - attack.t1555.003
logsource:
    product: windows
    category: file_event
detection:
    selection:
        TargetFilename|contains:
            - '\Google\Chrome\User Data\Default\Login Data'
            - '\Microsoft\Edge\User Data\Default\Login Data'
            - '\Mozilla\Firefox\Profiles\'
        TargetFilename|endswith:
            - 'Login Data'
            - 'logins.json'
    filter_legitimate:
        Image|contains:
            - '\chrome.exe'
            - '\msedge.exe'
            - '\firefox.exe'
    condition: selection and not filter_legitimate
falsepositives:
    - Backup software accessing browser profiles
    - Password manager extensions accessing credential stores
level: high
```
 
---
## Detection 5 — Cmdkey Credential Enumeration
 
**Technique:** T1555.004 — Windows Credential Manager
**Log source:** Sysmon Event ID 1
 
```yaml
title: Credential Manager Enumeration via Cmdkey
id: d39-005
status: experimental
description: Detects cmdkey being used to enumerate stored credentials in Windows Credential Manager
references:
    - https://attack.mitre.org/techniques/T1555/004/
author: Lawrence
date: 2026-07-07
tags:
    - attack.credential_access
    - attack.t1555.004
logsource:
    product: windows
    category: process_creation
detection:
    selection:
        Image|endswith: '\cmdkey.exe'
        CommandLine|contains: '/list'
    condition: selection
falsepositives:
    - IT admins legitimately checking stored credentials
    - Helpdesk troubleshooting credential issues
level: medium
```
