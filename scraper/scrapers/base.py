from abc import ABC, abstractmethod

from scrapers.model import Coupon


class BaseScraper(ABC):
    site_name: str

    @abstractmethod
    def scrape(self) -> list[Coupon]:
        pass
