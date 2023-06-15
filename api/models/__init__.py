from sqlalchemy import VARCHAR, Column, DateTime, Integer, Text

from database import Base


class Comments(Base):
    __tablename__ = "comments"

    id = Column(Integer, autoincrement=True, primary_key=True)
    live_chat_id = Column(VARCHAR(255), nullable=False)
    author_channel_id = Column(VARCHAR(255))
    author_profile_image_url = Column(VARCHAR(255))
    published_at = Column(DateTime)
    message_text = Column(Text)


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True)
    channel_id = Column(VARCHAR(255))


class Lives(Base):
    __tablename__ = "lives"

    id = Column(Integer, autoincrement=True, primary_key=True)
    live_chat_id = Column(VARCHAR(255), nullable=False)
