from datetime import datetime
from typing import Union

from pydantic import BaseModel


class Comment(BaseModel):
    id: int
    live_chat_id: str
    author_channel_id: str
    author_profile_image_url: str
    published_at: datetime
    message_text: str
    type: str
    display_name: str
    amount_micros: Union[int, None]
    currency: Union[str, None]

    class Config:
        orm_mode = True


class Live(BaseModel):
    id: int
    liver_id: int
    live_id: str
    start_time: datetime
    end_time: Union[datetime, None]
    live_chat_id: Union[str, None]
    page_token: Union[str, None]

    class Config:
        orm_mode = True


class Point(BaseModel):
    id: int
    listener_channel_id: str
    liver_id: int
    value: int

    class Config:
        orm_mode = True


class User(BaseModel):
    id: int
    channel_id: str
    profile_image_url: Union[str, None]
    wallet: Union[str, None]

    class Config:
        orm_mode = True
