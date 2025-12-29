from scrapers.base import BaseScraper


class DummyScraper(BaseScraper):
    site_name = "ExamplePage"

    def scrape(self):
        return [
            {
                "site": self.site_name,
                "store": "Demo Store",
                "description": "Save 10%",
                "discount": "10%",
                "code": "DEMO10",
                "expires_at": None,
                "store_logo": "https://example.com/logo.png",
                "url": "https://example.com"
            }
        ]
