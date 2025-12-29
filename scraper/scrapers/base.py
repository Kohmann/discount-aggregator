from abc import ABC, abstractmethod


class BaseScraper(ABC):
    site_name: str

    @abstractmethod
    def scrape(self) -> list[dict]:
        pass
