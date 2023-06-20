from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import services
from database import get_db

router = APIRouter()

TAGS = ["定期実行 (bot)"]


@router.post(
    "/cron/live",
    tags=TAGS,
)
async def get_and_register_comments(
    db: Session = Depends(get_db),
):
    """終了していないライブのコメントを取得してDB登録"""

    await services.get_and_register_comments(db)
    return {"status": "ok"}


@router.post(
    "/cron/live/end",
    tags=TAGS,
)
async def transfer_tokens_for_finished_live(
    db: Session = Depends(get_db),
):
    """終了したライブのポイントを精算してトークンを送信"""

    await services.transfer_tokens_for_finished_live(db)
    return {"status": "ok"}
