from scrapers.model import Discount
from scrapers.base import BaseScraper


class DummyScraper(BaseScraper):
    site_name = "ExamplePage"

    def scrape(self):
        return [
            Discount(
                site=self.site_name,
                store="Example Store",
                code="EXAMPLE2024",
                description="20% off on all items",
                discount="20%",
                expires_at=None,
                link="https://example.com/discount"
            ),
        ]

