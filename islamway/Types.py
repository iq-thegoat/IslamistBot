from pydantic import BaseModel
from typing import Optional
import datetime


class Nasheed(BaseModel):
    name:Optional[str]
    filename:Optional[str]
    publisher:Optional[str]
    publisher_profile:Optional[str]
    publisher_img:Optional[str]
    publish_date:Optional[datetime.datetime]
    views:Optional[int]
    likes:Optional[int]
    dislikes:Optional[int]
    nasheed_url:Optional[str]
    download_url:Optional[str]
    text:Optional[str]

class Fatwa(BaseModel):
    question:Optional[str]
    mufti:Optional[str]
    mufti_profile:Optional[str]
    mufti_img:Optional[str]
    publish_date:Optional[datetime.datetime]
    views:Optional[int]
    likes:Optional[int]
    dislikes:Optional[int]
    fatwa_url:Optional[str]
    answers:Optional[str]

