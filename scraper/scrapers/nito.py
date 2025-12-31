

import httpx
from bs4 import BeautifulSoup, Tag

from scrapers.base import BaseScraper
from scrapers.model import Discount

from scrapers.utils import generate_link



class NitoScraper(BaseScraper):
    site_name = "NITO"
    base_url = "https://www.nito.no"
    list_url = "https://www.nito.no/medlemskap-og-fordeler/medlemsfordeler/?category=Rabatter"


    def scrape(self) -> list[Discount]:
        discounts = []

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

        # Nito rabatt section
        target_img = soup.find("img", src="/Pictograms/rabatt.png")
        membership_discount_section = target_img.find_parent("section", class_="member-benefit-list__group")
        items = membership_discount_section.find_all("div", class_="article-teaser__content")

        for (idx, item) in enumerate(items):
            discount = self.scrape_item(item)
            if discount:
                discounts.append(discount)
            else:
                print(f"Failed to scrape item nr.{idx+1} from {len(items)} items")
        return discounts

    def scrape_item(self, item: Tag) -> Discount | None:
        try:
            store = item.find("div", class_="article-teaser__partner").find("img").get("alt")
            link = item.find("a", class_="article-teaser__link btn btn--with-arrow")
            description = link.get_text(strip=True)
            full_link = generate_link(self.base_url, link.get("href"))
            print(f"link: {full_link}")
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
