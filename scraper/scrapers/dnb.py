import httpx
from bs4 import BeautifulSoup, Tag

from scrapers.base import BaseScraper
from scrapers.model import Discount

class DnbScraper(BaseScraper):
    site_name = "DNB"
    base_url = "https://www.dnb.no"
    list_url = "https://www.dnb.no/kundeprogram/fordeler/faste-rabatter"


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

        # dnb rabatt section
        discount_code_element = soup.find("span", class_="css-o15es7 e19v4qza1")
        if not discount_code_element:
            raise ValueError(f"{self.site_name}: Could not find discount code element. The page structure may have changed.")
        static_discount_code = discount_code_element.get_text(strip=True)

        items = soup.find_all("a", class_="dnb-anchor--no-style dnb-anchor--no-hover dnb-anchor--no-underline etl9f1w0 css-19gq7c4 e1ig56cy0 dnb-anchor dnb-anchor--was-node dnb-a")
        if not items:
            raise ValueError(f"{self.site_name}: Could not find any discount items. The page structure may have changed.")

        for item in items:
            discounts.append(self.scrape_item(item, static_discount_code))
        return discounts

    def scrape_item(self, item: Tag, discount_code: str) -> Discount:
        store = item.find("h3", class_="dnb-heading dnb-h--medium css-5pbyeb etl9f1w4").get_text(strip=True)
        discount = item.find("span", class_="css-atp9e0 etl9f1w6").get_text(strip=True)
        description = discount + " by using code " + discount_code
        full_link = item.get("href")
        return Discount(
            site=self.site_name,
            store=store,
            description=description,
            discount=discount,
            code=discount_code,
            expires_at=None,
            link=full_link,
        )
