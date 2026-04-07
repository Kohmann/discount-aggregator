from bs4 import Tag

from scrapers.base import BaseScraper
from scrapers.model import Discount

from scrapers.utils import generate_link



class NitoScraper(BaseScraper):
    site_name = "NITO"
    base_url = "https://www.nito.no"
    list_url = "https://www.nito.no/medlemskap-og-fordeler/medlemsfordeler/?category=Rabatter"


    def scrape(self) -> list[Discount]:
        soup = self.fetch(self.list_url)

        target_img = soup.find("img", src="/Pictograms/rabatt.png")
        if not target_img:
            raise ValueError(f"{self.site_name}: Could not find anchor image 'rabatt.png'. The page structure may have changed.")
        membership_discount_section = target_img.find_parent("section", class_="member-benefit-list__group")
        if not membership_discount_section:
            raise ValueError(f"{self.site_name}: Could not find discount section. The page structure may have changed.")
        content_items = membership_discount_section.find_all("div", class_="article-teaser__content")
        if not content_items:
            raise ValueError(f"{self.site_name}: Could not find any discount items. The page structure may have changed.")

        items = [item.parent for item in content_items]

        return [self.scrape_item(item) for item in items]

    def scrape_item(self, item: Tag) -> Discount:
        partner_div = item.find("div", class_="article-teaser__partner")
        img = partner_div.find("img") if partner_div else None
        store = img.get("alt") if img else ""
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
