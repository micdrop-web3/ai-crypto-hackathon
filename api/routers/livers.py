from datetime import date
from typing import List, Union

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session, aliased

import schemas
import services
from database import get_db
from models import Comment, Live, Point, User

router = APIRouter()

TAGS = ["配信者向け"]


@router.post(
    "/live_chat/starts",
    tags=TAGS,
)
async def register_live(
    live_id: str,
    liver_channel_id: str,
    db: Session = Depends(get_db),
):
    """ライブを登録"""

    await services.register_live(live_id, liver_channel_id, db)
    return {"status": "ok"}


@router.get(
    "/ranking/points/group_by_user",
    tags=TAGS,
)
async def ranking_points(
    live_id: Union[str, None] = None,
    liver_channel_id: Union[str, None] = None,
    listener_channel_id: Union[str, None] = None,
    db: Session = Depends(get_db),
):
    """ポイントの合計ランキングを出力

    **ポイント ユーザのチャンネルID 画像URL, 名前**
    """

    return services.livers.ranking_points(
        live_id,
        liver_channel_id,
        listener_channel_id,
        db,
    )


@router.get(
    "/ranking/superchats/group_by_user",
    tags=TAGS,
)
async def ranking_superchats(
    live_id: Union[str, None] = None,
    liver_channel_id: Union[str, None] = None,
    listener_channel_id: Union[str, None] = None,
    db: Session = Depends(get_db),
):
    """スーパーチャットの合計ランキングを出力

    **スーパーチャット ユーザのチャンネルID 画像URL, 名前**

    JPYのみ
    """

    return services.livers.ranking_superchats(
        live_id,
        liver_channel_id,
        listener_channel_id,
        db,
    )


@router.get(
    "/ranking/comments/group_by_user",
    tags=TAGS,
)
async def ranking_comments(
    live_id: Union[str, None] = None,
    liver_channel_id: Union[str, None] = None,
    listener_channel_id: Union[str, None] = None,
    db: Session = Depends(get_db),
):
    return services.livers.ranking_superchats(
        live_id,
        liver_channel_id,
        listener_channel_id,
        db,
    )
