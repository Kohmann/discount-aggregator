from bs4 import Tag

from scrapers.base import BaseScraper
from scrapers.model import Discount
from scrapers.utils import generate_link


class ObosScraper(BaseScraper):
    site_name = "OBOS"
    base_url = "https://www.obos.no"
    list_url = "https://www.obos.no/medlem/medlemsfordeler?view=list"

    def scrape(self) -> list[Discount]:
        soup = self.fetch(self.list_url)

        items = soup.find_all("a", href=lambda x: x and x.startswith("/medlem/medlemsfordeler/"))
        if not items:
            raise ValueError(f"{self.site_name}: Could not find any discount items. The page structure may have changed.")

        return [self.scrape_item(item) for item in items]

    def scrape_item(self, item: Tag) -> Discount:
        store = item.find("h3").get_text(strip=True)
        description = item.find("p").get_text(strip=True)
        full_link = generate_link(self.base_url, item.get("href"))
        return Discount(
            store=store,
            description=description,
            discount=None,
            code=None,
            expires_at=None,
            link=full_link,
        )
