from bs4 import BeautifulSoup, Tag
from playwright.sync_api import sync_playwright

from scrapers.base import BaseScraper
from scrapers.model import Discount

from scrapers.utils import generate_link

_CONSENT_BUTTON_ID = "consent_prompt_submit"


class NitoScraper(BaseScraper):
    site_name = "NITO"
    base_url = "https://www.nito.no"
    list_url = "https://www.nito.no/medlemskap-og-fordeler/medlemsfordeler/?category=Rabatter"


    def fetch(self, url: str) -> BeautifulSoup:
        print(f"Fetching and scraping {self.site_name} website...")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            try:
                page = browser.new_page()
                page.goto(url, wait_until="domcontentloaded")
                consent_button = page.query_selector(f"#{_CONSENT_BUTTON_ID}")
                if consent_button:
                    consent_button.click()
                    page.wait_for_load_state("domcontentloaded")
                html = page.content()
            finally:
                browser.close()
        return BeautifulSoup(html, "lxml")


    def scrape(self) -> list[Discount]:
        soup = self.fetch(self.list_url)

        target_img = soup.find("img", src="/Pictograms/rabatt.png")
        if not target_img:
            raise ValueError(f"{self.site_name}: Could not find anchor image 'rabatt.png'. The page structure may have changed.")
        membership_discount_section = target_img.find_parent("section", class_="member-benefit-list__group")
        if not membership_discount_section:
            raise ValueError(f"{self.site_name}: Could not find discount section. The page structure may have changed.")
        items = membership_discount_section.find_all("div", class_="article-teaser__content")
        if not items:
            raise ValueError(f"{self.site_name}: Could not find any discount items. The page structure may have changed.")

        return [self.scrape_item(item) for item in items]

    def scrape_item(self, item: Tag) -> Discount:
        store = item.find("div", class_="article-teaser__partner").find("img").get("alt")
        link = item.find("a", class_="article-teaser__link btn btn--with-arrow")
        description = link.get_text(strip=True)
        full_link = generate_link(self.base_url, link.get("href"))
        return Discount(
            store=store,
            description=description,
            discount=None,
            code=None,
            expires_at=None,
            link=full_link,
        )
