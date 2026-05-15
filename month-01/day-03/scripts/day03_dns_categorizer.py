import argparse
import csv
import re
from collections import Counter
from pathlib import Path

QUERY_NAME_RE = re.compile(
    r"Standard query(?: response)? 0x[0-9a-fA-F]+ "
    r"(?:A|AAAA|CNAME|NS|MX|TXT|PTR|SRV|SOA|HTTPS|SVCB) "
    r"([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})"
)

FALLBACK_DOMAIN_RE = re.compile(r"([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})")

SYSTEM_SUFFIXES = [
    "contile.services.mozilla.com",
    "firefox.settings.services.mozilla.com",
    "cdn.mozilla.net",
    "ocsp.starfieldtech.com",
    "ocsp.sectigo.com",
    "ocsp.godaddy.com",
    "o.pki.goog",
    "pki.goog",
    "dns.google",
    "microsoft.com",
    "ubuntu.com",
    "apple.com",
    "wpad",
]

BROWSER_SUFFIXES = [
    "exploit-db.com",
    "example.org",
    "google.com",
    "withgoogle.com",
    "gstatic.com",
    "googleusercontent.com",
    "github.com",
    "githubassets.com",
    "githubusercontent.com",
    "githubcopilot.com",
    "wikipedia.org",
    "wikimedia.org",
    "reddit.com",
    "stackoverflow.com",
    "amazon.com",
]


def extract_domain(info_field: str) -> str:
    if not info_field:
        return ""

    match = QUERY_NAME_RE.search(info_field)
    if match:
        return match.group(1).lower().rstrip(".")

    match = FALLBACK_DOMAIN_RE.search(info_field)
    if match:
        return match.group(1).lower().rstrip(".")

    return ""


def matches_suffix(domain: str, suffix: str) -> bool:
    suffix = suffix.lower().rstrip(".")
    return domain == suffix or domain.endswith("." + suffix)


def categorize_domain(info_field: str) -> str:
    domain = extract_domain(info_field)
    if not domain:
        return "unknown"

    for suffix in SYSTEM_SUFFIXES:
        if matches_suffix(domain, suffix):
            return "system"

    for suffix in BROWSER_SUFFIXES:
        if matches_suffix(domain, suffix):
            return "browser"

    return "unknown"


def categorize_csv(input_csv: Path, output_csv: Path) -> Counter:
    rows = []
    counts = Counter()

    with input_csv.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError("Input CSV has no header row.")

        for row in reader:
            category = categorize_domain(row.get("Info", ""))
            row["Category"] = category
            rows.append(row)
            counts[category] += 1

    if not rows:
        raise ValueError("Input CSV has no data rows.")

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", encoding="utf-8", newline="") as f:
        fieldnames = list(rows[0].keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return counts


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Categorize DNS queries from a Wireshark CSV into system/browser/unknown."
    )
    parser.add_argument(
        "--input",
        default="day03-dnsList.csv",
        help="Path to input Wireshark DNS CSV (default: day03-dnsList.csv)",
    )
    parser.add_argument(
        "--output",
        default="day03-dns-categorized.csv",
        help="Path to output categorized CSV (default: day03-dns-categorized.csv)",
    )
    args = parser.parse_args()

    input_csv = Path(args.input).expanduser().resolve()
    output_csv = Path(args.output).expanduser().resolve()

    if not input_csv.exists():
        raise FileNotFoundError(f"Input CSV not found: {input_csv}")

    counts = categorize_csv(input_csv, output_csv)

    print(f"Categorized {sum(counts.values())} DNS rows")
    print(f"Saved to: {output_csv}")
    print("Breakdown:")
    for category in ("browser", "system", "unknown"):
        print(f"  {category}: {counts.get(category, 0)}")


if __name__ == "__main__":
    main()
