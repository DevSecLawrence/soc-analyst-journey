import "pe"
rule unusual_pe_sections {
    meta:
        description = "Detects ELF/PE files with UPX packer section names"
    condition:
        pe.is_pe and
        for any i in (0 .. pe.number_of_sections - 1) : (
            pe.sections[i].name == ".upx0" or
            pe.sections[i].name == ".upx1" or
            pe.sections[i].name == ".packed"
        )
}
