from bs4 import Tag

from scrapers.base import BaseScraper
from scrapers.model import Discount

from scrapers.utils import generate_link



class SkiforeningenScraper(BaseScraper):
    site_name = "Skiforeningen"
    base_url = "https://www.skiforeningen.no"
    list_url = "https://www.skiforeningen.no/medlemsskap/ditt-medlemskap/medlemsfordeler/"


    def scrape(self) -> list[Discount]:
        soup = self.fetch(self.list_url)

        items = soup.find_all("div", class_="standalone promoBlock")
        if not items:
            raise ValueError(f"{self.site_name}: Could not find any discount items. The page structure may have changed.")

        return [self.scrape_item(item) for item in items]

    def scrape_item(self, item: Tag) -> Discount:
        link = self.get_discount_link(item)
        store = link.get_text(strip=True)
        description = item.find("h2", class_="text-headline").get_text(strip=True)
        full_link = generate_link(self.base_url, link.get("href"))
        return Discount(
            store=store,
            description=description,
            discount=None,
            code=None,
            expires_at=None,
            link=full_link,
        )

    @staticmethod
    def get_discount_link(item: Tag) -> Tag | None:
        link = item.find("a", class_="text-action-onSecondaryContainer")
        if link:
            return link
        else:
            return item.find("a", class_="button-on-background")
