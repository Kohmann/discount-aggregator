import re

from bs4 import BeautifulSoup, Tag

from scrapers.base import BaseScraper
from scrapers.model import Discount

_DISCOUNT_CODE_HEADING = re.compile(r"Benytt rabattkode", re.IGNORECASE)


class DnbScraper(BaseScraper):
    site_name = "DNB"
    base_url = "https://www.dnb.no"
    list_url = "https://www.dnb.no/kundeprogram/fordeler/faste-rabatter"

    def scrape(self) -> list[Discount]:
        return self.parse(self.fetch(self.list_url))

    def parse(self, soup: BeautifulSoup) -> list[Discount]:
        discount_code = self._find_discount_code(soup)

        items = [a for a in soup.find_all("a", href=True) if self._is_discount_card(a)]
        if not items:
            raise ValueError(f"{self.site_name}: Could not find any discount items. The page structure may have changed.")

        return [self.scrape_item(item, discount_code) for item in items]

    def _find_discount_code(self, soup: BeautifulSoup) -> str:
        heading = soup.find(["h2", "h3"], string=_DISCOUNT_CODE_HEADING)
        code_element = heading.find_next("span") if heading else None
        if not code_element or not code_element.get_text(strip=True):
            raise ValueError(f"{self.site_name}: Could not find discount code element. The page structure may have changed.")
        return code_element.get_text(strip=True)

    @staticmethod
    def _is_discount_card(anchor: Tag) -> bool:
        # A discount card is a link whose first child is the discount badge and which has a store heading.
        first_child = anchor.find(recursive=False)
        return first_child is not None and first_child.name == "span" and anchor.find("h3") is not None

    def scrape_item(self, item: Tag, discount_code: str) -> Discount:
        store = item.find("h3").get_text(strip=True)
        discount = re.sub(r"\s+%", "%", item.find("span", recursive=False).get_text(strip=True))
        description = discount + " by using code " + discount_code
        return Discount(
            store=store,
            description=description,
            discount=discount,
            code=discount_code,
            expires_at=None,
            link=self._normalize_link(item.get("href")),
        )

    @staticmethod
    def _normalize_link(href: str) -> str:
        href = href.strip().rstrip(".")
        if not href.startswith("http"):
            href = "https://" + href.lstrip("/")
        return href
