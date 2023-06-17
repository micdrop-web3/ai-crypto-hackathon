from sqlalchemy import VARCHAR, Column, DateTime, ForeignKey, Integer, Text

from database import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, autoincrement=True, primary_key=True)
    live_chat_id = Column(VARCHAR(255), nullable=False)
    author_channel_id = Column(VARCHAR(255))
    author_profile_image_url = Column(VARCHAR(255))
    published_at = Column(DateTime)
    message_text = Column(Text)
    type = Column(VARCHAR(255))
    display_name = Column(Text)
    amount_micros = Column(Integer)
    currency = Column(VARCHAR(255))


class Live(Base):
    __tablename__ = "lives"

    id = Column(Integer, autoincrement=True, primary_key=True)
    liver_id = Column(
        Integer,
        ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"),
    )
    live_id = Column(VARCHAR(255))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    # ライブ中のみ使う
    live_chat_id = Column(VARCHAR(255))
    page_token = Column(VARCHAR(255))


class Point(Base):
    __tablename__ = "points"

    id = Column(Integer, autoincrement=True, primary_key=True)
    listener_channel_id = Column(VARCHAR(255))
    liver_id = Column(
        Integer,
        ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"),
    )
    value = Column(Integer, default=0)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True)
    channel_id = Column(VARCHAR(255))
    profile_image_url = Column(VARCHAR(255))
    wallet = Column(VARCHAR(255))
