from scrapers.dummy import DummyScraper
from pathlib import Path
import re
from datetime import datetime

from scrapers.model import Coupon
from scrapers.obos import ObosScraper

README_PATH = Path(__file__).parent.parent / "README.md"


def coupons_to_markdown(coupons: list[Coupon]) -> str:
    headers = ["Store", "Description", "Source"]

    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |"
    ]

    for c in coupons:
        lines.append(
            f"| {c.store} | {c.description} | [Link]({c.link}) |"
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
        # DummyScraper(),
        ObosScraper(),
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
