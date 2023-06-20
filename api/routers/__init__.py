from typing import List, Union

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, aliased

import schemas
from database import get_db
from models import Comment, Live, Point, User

router = APIRouter()

TAGS = ["汎用"]


@router.get(
    "/comments/list",
    response_model=List[schemas.Comment],
    tags=TAGS,
)
async def list_comments(
    live_id: Union[str, None] = None,
    author_channel_id: Union[str, None] = None,
    type: Union[str, None] = None,
    offset: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """コメントを取得"""

    comments = (
        db.query(Comment)
        .filter(
            True if live_id is None else Comment.live_id == live_id,
        )
        .filter(
            True
            if author_channel_id is None
            else Comment.author_channel_id == author_channel_id,
        )
        .order_by(Comment.published_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return [schemas.Comment.from_orm(comment) for comment in comments]


@router.get(
    "/lives/list",
    response_model=List[schemas.Live],
    tags=TAGS,
)
async def list_lives(
    live_id: Union[str, None] = None,
    liver_channel_id: Union[str, None] = None,
    offset: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    Liver = aliased(User)
    lives = (
        db.query(Live)
        .join(Liver, Liver.id == Live.liver_id)
        .filter(
            True if live_id is None else Live.live_id == live_id,
            True
            if liver_channel_id is None
            else Liver.channel_id == liver_channel_id,
        )
        .order_by(Live.start_time.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return [schemas.Live.from_orm(live) for live in lives]


@router.get(
    "/points/list",
    response_model=List[schemas.Point],
    tags=TAGS,
)
async def list_points(
    db: Session = Depends(get_db),
):
    points = db.query(Point).all()
    return [schemas.Point.from_orm(point) for point in points]


@router.get(
    "/users/list",
    response_model=List[schemas.User],
    tags=TAGS,
)
async def list_users(
    db: Session = Depends(get_db),
):
    users = db.query(User).all()
    return [schemas.User.from_orm(user) for user in users]
