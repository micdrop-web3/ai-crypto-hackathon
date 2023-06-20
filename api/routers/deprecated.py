from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy import func
from sqlalchemy.orm import Session, aliased

import schemas
from database import get_db
from models import Comment, Live, Point, User

router = APIRouter()

TAGS = ["その他"]


@router.get("/", tags=TAGS)
async def redirect_document():
    return RedirectResponse(url="api/docs")


@router.get(
    "/user/comments/last",
    response_model=List[schemas.Comment],
    tags=TAGS,
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
    tags=TAGS,
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
    tags=TAGS,
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
    tags=TAGS,
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
    tags=TAGS,
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


@router.get(
    "/ranking/liver",
    tags=TAGS,
)
async def ranking_liver(
    liver_channel_id: str,
    db: Session = Depends(get_db),
):
    """ある配信者ポイントの獲得ランキング"""
    Liver = aliased(User)
    Listener = aliased(User)

    ranking = (
        db.query(Point, Listener)
        .join(Liver, Liver.id == Point.liver_id)
        .outerjoin(
            Listener,
            Listener.channel_id == Point.listener_channel_id,
        )
        .filter(
            Liver.channel_id == liver_channel_id,
        )
        .order_by(Point.value.desc())
        .limit(100)
        .all()
    )
    return [(pt.value, pt.listener_channel_id) for pt, lnr in ranking]


@router.get(
    "/ranking/comment_count",
    tags=TAGS,
)
async def ranking_comment_count(
    liver_channel_id: str,
    db: Session = Depends(get_db),
):
    """ある配信者コメント回数ランキング"""
    Liver = aliased(User)
    Listener = aliased(User)

    ranking = (
        db.query(
            func.count(Comment.author_channel_id),
            Comment.author_channel_id,
            Listener,
        )
        .join(Live, Live.live_chat_id == Comment.live_chat_id)
        .join(Liver, Liver.id == Live.liver_id)
        .outerjoin(
            Listener,
            Listener.channel_id == Comment.author_channel_id,
        )
        .filter(
            Liver.channel_id == liver_channel_id,
        )
        .group_by(Comment.author_channel_id, Listener.id)
        .order_by(func.count(Comment.author_channel_id).desc())
        .limit(100)
        .all()
    )
    return [
        (count, channel_id, lsnr.profile_image_url if lsnr else "")
        for count, channel_id, lsnr in ranking
    ]
