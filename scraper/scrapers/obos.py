import httpx
import re
from bs4 import BeautifulSoup

from scrapers.base import BaseScraper
from scrapers.model import Discount


class ObosScraper(BaseScraper):
    site_name = "OBOS"
    base_url = "https://www.obos.no"
    list_url = "https://www.obos.no/medlem/medlemsfordeler?view=list"

    def scrape(self) -> list[Discount]:
        coupons = []

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "nb-NO,nb;q=0.9,en-US;q=0.8,en;q=0.7"
        }

        try:
            # Use httpx to fetch the page
            print(f"Fetching and scraping {self.site_name} website...")
            response = httpx.get(self.list_url, headers=headers, follow_redirects=True, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "lxml")

            # OBOS target: the <a> tags under the membership benefits section
            items = soup.find_all("a", href=lambda x: x and x.startswith("/medlem/medlemsfordeler/"))

            for item in items:
                store = item.find("h3").get_text(strip=True)
                description = item.find("p").get_text(strip=True)

                link = self.base_url + item.get("href")

                coupons.append(
                    Discount(
                        site=self.site_name,
                        store=store,
                        description=description,
                        discount=None,
                        code=None,
                        expires_at=None,  # Ongoing
                        link=link
                    )
                )

        except Exception as e:
            print(f"Error scraping {self.site_name}: {e}")
            return []

        return coupons
