import re
from datetime import datetime
from pathlib import Path

from scrapers.model import Discount
from scrapers.obos import ObosScraper
from scrapers.skiforeningen import SkiforeningenScraper

README_PATH = Path(__file__).parent.parent / "README.md"


def discounts_to_markdown(discounts: list[Discount]) -> str:
    headers = ["Store", "Description", "Source"]

    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]

    for d in discounts:
        lines.append(f"| {d.store} | {d.description} | [Link]({d.link}) |")

    return "\n".join(lines)


def update_readme(table: str):
    content = README_PATH.read_text()

    updated = re.sub(
        r"<!-- DISCOUNTS_START -->.*?<!-- DISCOUNTS_END -->",
        f"<!-- DISCOUNTS_START -->\n{table}\n<!-- DISCOUNTS_END -->",
        content,
        flags=re.S,
    )

    README_PATH.write_text(updated)


def main():
    scrapers = [
        ObosScraper(),
        SkiforeningenScraper(),
    ]

    discounts = []
    for scraper in scrapers:
        discounts.extend(scraper.scrape())

    discounts.sort(key=lambda d: d.store.lower())  # Sort alphabetically by store name
    table = discounts_to_markdown(discounts)
    update_readme(table)
    print(f"Updated README with {len(discounts)} discounts at {datetime.now()}")


if __name__ == "__main__":
    main()
