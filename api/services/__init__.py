import os
from datetime import datetime, timedelta

import googleapiclient.discovery
import googleapiclient.errors
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session, aliased

from database import get_db
from models import Comment, Live, Point, User

from .tokens import get_web3_client, transfer_erc20


async def register_live(live_id, liver_channel_id, db):
    """ライブをDBに登録"""

    live = db.query(Live).filter(Live.live_id == live_id).first()
    if live:
        # すでに登録済
        raise HTTPException(
            status_code=400,
            detail="live has been registered",
        )

    live = await get_live_from_yt(
        live_id,
        client=await get_youtube_client(),
    )
    liver = db.query(User).filter(User.channel_id == liver_channel_id).first()
    if not liver:
        raise HTTPException(
            status_code=400,
            detail="invalid channel id",
        )
    live.liver_id = liver.id
    db.add(live)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise


async def get_youtube_client():
    client = googleapiclient.discovery.build(
        serviceName="youtube",
        version="v3",
        developerKey=os.getenv("YOUTUBE_DATA_API_KEY"),
    )

    return client


async def get_live_from_yt(live_id: str, client=Depends(get_youtube_client)):
    payload = {
        "part": "liveStreamingDetails",
        "id": live_id,
    }
    res = client.videos().list(**payload).execute()

    v_item = list(
        filter(
            lambda item: item.get("kind") == "youtube#video",
            res.get("items", []),
        )
    )

    if len(v_item) == 0:
        raise HTTPException(status_code=404, detail="item not found")

    details = v_item[0]["liveStreamingDetails"]
    live = Live(
        live_id=live_id,
        start_time=str2datetime(details["actualStartTime"]),
        end_time=str2datetime(details.get("actualEndTime")),
        live_chat_id=details.get("activeLiveChatId"),
    )

    return live


async def get_live_for_update(
    live_id: str,
    db: Session = Depends(get_db),
):
    return (
        db.query(Live)
        .filter(Live.live_id == live_id)
        .with_for_update()
        .first()
    )


def item2Comment(cmt, live_id):
    c = Comment(
        live_id=live_id,
        live_chat_id=cmt["snippet"]["liveChatId"],
        author_channel_id=cmt["snippet"]["authorChannelId"],
        author_profile_image_url=cmt["authorDetails"]["profileImageUrl"],
        published_at=str2datetime(cmt["snippet"]["publishedAt"]),
        message_text=cmt["snippet"]["displayMessage"],
        type=cmt["snippet"]["type"],
        display_name=cmt["authorDetails"]["displayName"],
    )
    if c.type == "superChatEvent":
        c.amount_micros = int(
            cmt["snippet"]["superChatDetails"]["amountMicros"]
        )
        c.currency = cmt["snippet"]["superChatDetails"]["currency"]
    return c


def update_point(point, cmt):
    """コメントの種類に応じてポイント加算"""

    if cmt.type in ["textMessageEvent", "superChatEvent"]:
        # 通常のコメント: 1pt
        # スーパーチャット: 1pt
        point.value += 1
    elif cmt.type == "memberMilestoneChatEvent":
        point.value += 100


async def get_and_register_comments_for_live(
    live_id: str,
    client=Depends(get_youtube_client),
    db: Session = Depends(get_db),
):
    # 悲観的ロック, readもできない
    live = await get_live_for_update(live_id, db)

    payload = {
        "part": "authorDetails,snippet",
        "liveChatId": live.live_chat_id,
        "pageToken": live.page_token,
    }
    try:
        res = client.liveChatMessages().list(**payload).execute()
    except googleapiclient.errors.HttpError:
        live_yt = await get_live_from_yt(live_id, client)
        if live_yt.end_time:
            # ライブ終了
            live.end_time = live_yt.end_time
            live.page_token = None
            db.commit()
            return
        raise

    live.page_token = res["nextPageToken"]

    cmts = [item2Comment(cmt, live.live_id) for cmt in res["items"]]
    db.add_all(cmts)

    ids = set(cmt.author_channel_id for cmt in cmts)
    exist_points = (
        db.query(Point)
        .filter(
            Point.live_id == live.live_id,
            Point.listener_channel_id.in_(ids),
        )
        .all()
    )
    not_exist = ids - set(point.listener_channel_id for point in exist_points)
    add_points = [
        Point(
            listener_channel_id=channel_id,
            live_id=live.live_id,
            liver_id=live.liver_id,
            value=0,
        )
        for channel_id in not_exist
    ]
    db.add_all(add_points)

    points = {}
    points.update({p.listener_channel_id: p for p in exist_points})
    points.update({p.listener_channel_id: p for p in add_points})

    msg = []
    for cmt in cmts:
        point = points.get(cmt.author_channel_id)
        update_point(point, cmt)
        msg.append(cmt.message_text)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise ValueError(",".join(msg))


async def get_and_register_comments(
    db: Session = Depends(get_db),
):
    """終了していないライブのコメントを取得してDB登録"""

    # 終了していないライブを列挙
    client = await get_youtube_client()
    lives = db.query(Live).filter(Live.end_time.is_(None)).all()
    for live in lives:
        # APIの限界がわからないので1個ずつ処理
        await get_and_register_comments_for_live(live.live_id, client, db)


async def transfer_token_as_point(
    point: Point,
    listener: User,
    live: Live,
    liver: User,
    client,
    db: Session = Depends(get_db),
):
    point_update = (
        db.query(Point).filter(Point.id == point.id).with_for_update().first()
    )
    tx_hash = transfer_erc20(
        client=client,
        contract_addr=liver.erc20_address,
        to_addr=listener.wallet,
        value=point_update.value * (10**6),
    )
    point_update.paid_out_tx = tx_hash
    db.commit()


async def transfer_tokens_for_finished_live(
    db: Session = Depends(get_db),
):
    """終了したライブのポイントを精算してトークンを送信"""

    Liver = aliased(User)
    Listener = aliased(User)

    # 終了したライブのポイントを列挙
    res = (
        db.query(Point, Liver, Listener)
        .join(Listener, Listener.channel_id == Point.listener_channel_id)
        .join(Live, Live.live_id == Point.live_id)
        .join(Liver, Liver.id == Live.liver_id)
        .filter(
            Point.paid_out_tx.is_(None),
            Listener.wallet.isnot(None),
            Liver.erc20_address.isnot(None),
            Live.end_time.isnot(None),
        )
        .all()
    )
    client = get_web3_client()
    for point, listener, live, liver in res:
        await transfer_token_as_point(point, listener, live, liver, client, db)


def str2datetime(datetime_s):
    if not datetime_s:
        return None

    return datetime.strptime(
        datetime_s[:19],
        "%Y-%m-%dT%H:%M:%S",
    ) + timedelta(hours=9)
