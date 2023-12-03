from pydantic import BaseModel
from typing import Optional
import datetime

class Hadith(BaseModel):
    """
    Pydantic model for representing information about a hadith.
    """
    text:Optional[str]
    narrator:Optional[str]
    page:Optional[str or int]
    muhadith:Optional[str]
    ruling:Optional[str]
    source:Optional[str]
    url:Optional[str]
    sharh:Optional[str]

    def __hash__(self):
        return hash(self.url)

    def __eq__(self, other):
        if isinstance(other, Hadith):
            if other.url == None and Hadith.url == None:
                return False
            return self.url == other.url
        return False
