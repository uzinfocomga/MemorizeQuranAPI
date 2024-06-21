from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, false
from sqlalchemy.orm import relationship

from .database import Base, engine

default_utc_time = lambda: datetime.utcnow() + timedelta(hours=5)

class User(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    chat_id = Column(Integer)
    full_name = Column(String, unique=False, nullable=False)
    username = Column(String, unique=True, nullable=False)
    language = Column(String, nullable=False, default='en')
    pending_chapter_id = Column(Integer, default=114)
    pending_page_id = Column(Integer, default=1)
    joined_at = Column(DateTime, default=default_utc_time)