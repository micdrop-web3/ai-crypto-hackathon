from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, aliased

import schemas
import services
from database import get_db
from models import Comment, Live, Point, User

router = APIRouter()


@router.post(
    "/live_chat/starts",
)
async def register_live(
    live_id: str,
    liver_channel_id: str,
    db: Session = Depends(get_db),
):
    """ライブを登録"""

    await services.register_live(live_id, liver_channel_id, db)
    return {"status": "ok"}


@router.post(
    "/cron/live",
)
async def get_and_register_comments(
    db: Session = Depends(get_db),
):
    """終了していないライブのコメントを取得してDB登録"""

    await services.get_and_register_comments(db)
    return {"status": "ok"}


@router.get(
    "/user/comments/last",
    response_model=List[schemas.Comment],
)
async def list_last_comments_for_user(
    channel_id: str,
    num: int = 100,
    db: Session = Depends(get_db),
):
    """最新のnum個のコメントを列挙"""
    cmts = (
        db.query(Comment)
        .filter(
            Comment.author_channel_id == channel_id,
        )
        .order_by(Comment.published_at.desc())
        .limit(num)
    )
    return [schemas.Comment.from_orm(cmt) for cmt in cmts]


@router.get(
    "/user/comments/list",
    response_model=List[schemas.Comment],
)
async def list_comments_for_user(
    channel_id: str,
    page: int = 1,
    per_page: int = 100,
    db: Session = Depends(get_db),
):
    cmts = (
        db.query(Comment)
        .filter(
            Comment.author_channel_id == channel_id,
        )
        .order_by(Comment.published_at.desc())
        .offset(per_page * (page - 1))
        .limit(per_page)
    )
    return [schemas.Comment.from_orm(cmt) for cmt in cmts]


@router.get(
    "/live/comments/last",
    response_model=List[schemas.Comment],
)
async def list_last_comments_for_live(
    live_chat_id: str,
    num: int = 100,
    db: Session = Depends(get_db),
):
    """最新のnum個のコメントを列挙"""
    cmts = (
        db.query(Comment)
        .filter(
            Comment.live_chat_id == live_chat_id,
        )
        .order_by(Comment.published_at.desc())
        .limit(num)
    )
    return [schemas.Comment.from_orm(cmt) for cmt in cmts]


@router.get(
    "/live/comments/list",
    response_model=List[schemas.Comment],
)
async def list_live_comments_for_live(
    live_chat_id: str,
    page: int = 1,
    per_page: int = 100,
    db: Session = Depends(get_db),
):
    cmts = (
        db.query(Comment)
        .filter(
            Comment.live_chat_id == live_chat_id,
        )
        .order_by(Comment.published_at.desc())
        .offset(per_page * (page - 1))
        .limit(per_page)
    )
    return [schemas.Comment.from_orm(cmt) for cmt in cmts]


@router.get(
    "/user/point",
    response_model=int,
)
async def list_point_for_user(
    channel_id: str,
    liver_channel_id: str,
    db: Session = Depends(get_db),
):
    """ユーザの所有ポイント"""
    Liver = aliased(User)

    point = (
        db.query(Point)
        .join(Liver, Liver.id == Point.liver_id)
        .filter(
            Liver.channel_id == liver_channel_id,
            Point.listener_channel_id == channel_id,
        )
        .first()
    )
    return point.value


@router.put(
    "/user",
)
async def read_user(
    channel_id: str,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.channel_id == channel_id).first()
    return schemas.User.from_orm(user)


@router.post(
    "/users",
)
async def put_user(
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
    "/comments/list",
    response_model=List[schemas.Comment],
)
async def list_comments(
    db: Session = Depends(get_db),
):
    comments = db.query(Comment).all()
    return [schemas.Comment.from_orm(comment) for comment in comments]


@router.get(
    "/lives/list",
    response_model=List[schemas.Live],
)
async def list_lives(
    db: Session = Depends(get_db),
):
    lives = db.query(Live).all()
    return [schemas.Live.from_orm(live) for live in lives]


@router.get(
    "/points/list",
    response_model=List[schemas.Point],
)
async def list_points(
    db: Session = Depends(get_db),
):
    points = db.query(Point).all()
    return [schemas.Point.from_orm(point) for point in points]


@router.get(
    "/users/list",
    response_model=List[schemas.User],
)
async def list_users(
    db: Session = Depends(get_db),
):
    users = db.query(User).all()
    return [schemas.User.from_orm(user) for user in users]
