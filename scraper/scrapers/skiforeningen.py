import httpx
from bs4 import BeautifulSoup, Tag

from scrapers.base import BaseScraper
from scrapers.model import Discount

from scrapers.utils import generate_link



class SkiforeningenScraper(BaseScraper):
    site_name = "Skiforeningen"
    base_url = "https://www.skiforeningen.no"
    list_url = (
        "https://www.skiforeningen.no/medlemsskap/ditt-medlemskap/medlemsfordeler/"
    )

    def scrape(self) -> list[Discount]:
        coupons = []

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "nb-NO,nb;q=0.9,en-US;q=0.8,en;q=0.7",
        }

        # Use httpx to fetch the page
        print(f"Fetching and scraping {self.site_name} website...")
        response = httpx.get(
            self.list_url, headers=headers, follow_redirects=True, timeout=15
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        # Skiforeningen target: div with class = "standalone promoBlock"
        items = soup.find_all("div", class_="standalone promoBlock")
        for item in items:
            discount = self.scrape_item(item)
            if discount:
                coupons.append(discount)

        return coupons

    def scrape_item(self, item: Tag) -> Discount | None:
        try:
            link = self.get_discount_link(item)
            store = link.get_text(strip=True)
            description = item.find("h2", class_="text-headline").get_text(strip=True)
            full_link = generate_link(self.base_url, link.get("href"))
            return Discount(
                site=self.site_name,
                store=store,
                description=description,
                discount=None,
                code=None,
                expires_at=None,
                link=full_link,
            )
        except Exception as e:
            print(f"Error scraping item. Skipping...  {e}")
            return None

    @staticmethod
    def get_discount_link(item: Tag) -> Tag | None:
        link = item.find("a", class_="text-action-onSecondaryContainer")
        if link:
            return link
        else:
            return item.find("a", class_="button-on-background")
