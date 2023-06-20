from typing import Union

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import schemas
from database import get_db
from models import Comment, User

router = APIRouter()

TAGS = ["ユーザ画面（視聴者・配信者共通）"]


@router.post(
    "/users",
    tags=TAGS,
)
async def create_user(
    channel_id: str,
    db: Session = Depends(get_db),
):
    """ユーザ情報を作成"""
    user = User(
        channel_id=channel_id,
    )
    db.add(user)
    db.commit()


@router.get(
    "/user",
    tags=TAGS,
)
async def read_user(
    channel_id: str,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.channel_id == channel_id).first()
    s_user = schemas.User.from_orm(user)
    if not s_user.name or not s_user.profile_image_url:
        cmt = (
            db.query(Comment)
            .filter(Comment.author_channel_id == channel_id)
            .order_by(Comment.published_at.desc())
            .first()
        )
        if cmt:
            s_user.name = s_user.name or cmt.display_name
            s_user.profile_image_url = (
                s_user.profile_image_url or cmt.profile_image_url
            )
    return s_user


@router.put(
    "/user",
    tags=TAGS,
)
async def update_user(
    channel_id: str,
    name: Union[str, None] = None,
    profile_image_url: Union[str, None] = None,
    wallet: Union[str, None] = None,
    erc20_address: Union[str, None] = None,
    db: Session = Depends(get_db),
):
    """ユーザ情報を作成"""
    user = (
        db.query(User)
        .filter(User.channel_id == channel_id)
        .with_for_update()
        .first()
    )
    if name:
        user.name = name
    if profile_image_url:
        user.profile_image_url = profile_image_url
    if wallet:
        user.wallet = wallet
    if erc20_address:
        user.erc20_address = erc20_address
    db.commit()
