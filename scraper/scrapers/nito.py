

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
        if not target_img:
            raise ValueError(f"{self.site_name}: Could not find anchor image 'rabatt.png'. The page structure may have changed.")
        membership_discount_section = target_img.find_parent("section", class_="member-benefit-list__group")
        if not membership_discount_section:
            raise ValueError(f"{self.site_name}: Could not find discount section. The page structure may have changed.")
        items = membership_discount_section.find_all("div", class_="article-teaser__content")
        if not items:
            raise ValueError(f"{self.site_name}: Could not find any discount items. The page structure may have changed.")

        for item in items:
            discounts.append(self.scrape_item(item))
        return discounts

    def scrape_item(self, item: Tag) -> Discount:
        store = item.find("div", class_="article-teaser__partner").find("img").get("alt")
        link = item.find("a", class_="article-teaser__link btn btn--with-arrow")
        description = link.get_text(strip=True)
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
