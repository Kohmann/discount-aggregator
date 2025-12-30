from abc import ABC, abstractmethod

from scrapers.model import Discount


class BaseScraper(ABC):
    site_name: str

    @abstractmethod
    def scrape(self) -> list[Discount]:
        pass
