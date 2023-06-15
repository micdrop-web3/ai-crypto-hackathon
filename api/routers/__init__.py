from typing import List, Union

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import Comments as mComments
from schemas.comments import Comments as sComments

router = APIRouter()


@router.post(
    "/live_chat/starts",
)
async def start__live_chat(
    db: Session = Depends(get_db),
):
    """ライブチャットを開始"""
    pass


@router.get(
    "/user/comments/last",
    response_model=List[sComments],
)
async def list_last_comments(
    channel_id: str,
    num: int,
    db: Session = Depends(get_db),
):
    """最新のnum個のコメントを列挙"""
    pass


@router.get(
    "/user/comments/list",
    response_model=List[sComments],
)
async def list_comments(
    channel_id: str,
    page: int = 1,
    per_page: int = 100,
    db: Session = Depends(get_db),
):
    pagi = (
        db.query(mComments)
        .filter(
            mComments.author_channel_id == channel_id,
        )
        .pagenate(page=page, per_page=per_page, error_out=True)
    )
    return [sComments(cmt) for cms in pagi.items]


@router.get(
    "/live/comments/last",
    response_model=List[sComments],
)
async def list_last_comments(
    live_chat_id: str,
    num: int,
    db: Session = Depends(get_db),
):
    """最新のnum個のコメントを列挙"""
    pass


@router.get(
    "/live/comments/list",
    response_model=List[sComments],
)
async def list_comments(
    live_chat_id: str,
    page: int = 1,
    per_page: int = 100,
    db: Session = Depends(get_db),
):
    pagi = (
        db.query(mComments)
        .filter(
            mComments.live_chat_id == live_chat_id,
        )
        .pagenate(page=page, per_page=per_page, error_out=True)
    )
    return [sComments(cmt) for cms in pagi.items]


@router.get(
    "/user/point",
    response_model=int,
)
async def list_comments(
    channel_id: str,
    db: Session = Depends(get_db),
):
    """ユーザの所有ポイント"""
    pass


@router.put(
    "/users",
    response_model=int,
)
async def put_user(
    channel_id: str,
    db: Session = Depends(get_db),
):
    """ユーザ情報を編集"""
    pass
