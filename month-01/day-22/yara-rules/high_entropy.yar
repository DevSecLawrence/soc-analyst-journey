import "math"
rule high_entropy_file {
    meta:
        description = "Flags files with entropy above 7.0 — possible packing or encryption"
    condition:
        math.entropy(0, filesize) > 7.0
}

