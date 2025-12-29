from scrapers.DummyScraper import DummyScraper
from pathlib import Path
import re
from datetime import datetime

README_PATH = Path(__file__).parent.parent / "README.md"

def coupons_to_markdown(coupons: list[dict]) -> str:
    headers = ["Store", "Description", "Code", "Expires", "Source"]

    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |"
    ]

    for c in coupons:
        lines.append(
            "| "
            + " | ".join([
                c["store"],
                c["description"],
                c["code"] or "-",
                c["expires_at"] or "-",
                f"[{c['site']}]({c['url']})"
            ])
            + " |"
        )

    return "\n".join(lines)

def update_readme(table: str):
    content = README_PATH.read_text()

    updated = re.sub(
        r"<!-- COUPONS_START -->.*?<!-- COUPONS_END -->",
        f"<!-- COUPONS_START -->\n{table}\n<!-- COUPONS_END -->",
        content,
        flags=re.S
    )

    README_PATH.write_text(updated)

def main():
    scrapers = [
        DummyScraper(),
    ]

    coupons = []
    for scraper in scrapers:
        try:
            coupons.extend(scraper.scrape())
        except Exception as e:
            print(f"Failed {scraper.site_name}: {e}")

    table = coupons_to_markdown(coupons)
    update_readme(table)

    print(f"Updated README with {len(coupons)} coupons at {datetime.utcnow()}")

if __name__ == "__main__":
    main()
