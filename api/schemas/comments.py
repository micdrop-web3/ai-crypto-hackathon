from datetime import datetime

from pydantic import BaseModel


class Comments(BaseModel):
    id: int
    live_chat_id: str
    author_channel_id: str
    author_profile_image_url: str
    published_at: datetime
    message_text: str


class Lives(BaseModel):
    id: int
    user_id: int
    live_chat_id: str


class Users(BaseModel):
    id: int
    channel_id: str
