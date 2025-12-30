from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Discount:
    site: str
    store: str
    code: Optional[str]
    description: str
    discount: Optional[str]
    expires_at: Optional[date]
    link: str
