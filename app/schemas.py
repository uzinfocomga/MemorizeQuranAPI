from datetime import datetime
from typing import List

from pydantic import BaseModel


class UserCreate(BaseModel):
    chat_id: int
    full_name: str
    username: str


# class UserUpdate(BaseModel):
#     pending_hadith_id: int


class UserOutput(UserCreate):
    id: int
    language: str
    pending_chapter_id: int
    pending_page_id: int
    joined_at: datetime


class UserOutputAll(BaseModel):
    users: List[UserOutput]