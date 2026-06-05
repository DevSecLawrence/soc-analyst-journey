rule suspicious_strings {
    meta:
        description = "Detects files referencing cmd.exe or powershell"
        author = "your name"
    strings:
        $a = "cmd.exe" nocase
        $b = "powershell.exe" nocase
    condition:
        any of them
}
