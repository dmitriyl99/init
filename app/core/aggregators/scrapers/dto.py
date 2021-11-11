from typing import Optional
from datetime import date


class ScrappedEvent:
    title: str
    date: Optional[str]
    short_description: Optional[str]
    description: Optional[str]
    place: Optional[str]
    image_url: Optional[str]

    def __init__(self, title: str,
                 date: Optional[str],
                 short_description: Optional[str] = None,
                 description: Optional[str] = None,
                 place: Optional[str] = None,
                 image_url: Optional[str] = None):
        self.title = title
        self.date = date
        self.short_description = short_description
        self.description = description
        self.place = place
        self.image_url = image_url
