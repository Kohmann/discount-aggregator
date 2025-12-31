

def generate_link(base_url:str, href: str | None) -> str:
    is_different_domain = href.startswith("http")
    if is_different_domain:
        return href
    return base_url + href