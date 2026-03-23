import httpx
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup

from scrapers.model import Discount

_DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "nb-NO,nb;q=0.9,en-US;q=0.8,en;q=0.7",
}


class BaseScraper(ABC):
    site_name: str

    def fetch(self, url: str) -> BeautifulSoup:
        print(f"Fetching and scraping {self.site_name} website...")
        response = httpx.get(url, headers=_DEFAULT_HEADERS, follow_redirects=True, timeout=15)
        response.raise_for_status()
        return BeautifulSoup(response.text, "lxml")

    @abstractmethod
    def scrape(self) -> list[Discount]:
        pass
