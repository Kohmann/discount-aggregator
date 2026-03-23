def generate_link(base_url: str, href: str | None) -> str:
    if href is None:
        return base_url
    if href.startswith("http"):
        return href
    return base_url + href