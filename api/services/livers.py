import os
from datetime import datetime, timedelta

import googleapiclient.discovery
import googleapiclient.errors
from fastapi import Depends, HTTPException
from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session, aliased

from database import get_db
from models import Comment, Live, Point, User


def ranking_points(
    live_id,
    liver_channel_id,
    listener_channel_id,
    db,
):
    Liver = aliased(User)
    Listener = aliased(User)

    ranking = (
        db.query(
            func.sum(Point.value),
            Point.listener_channel_id,
            Listener.profile_image_url,
            Listener.name,
        )
        .join(Liver, Liver.id == Point.liver_id)
        .join(Live, Live.live_id == Point.live_id)
        .outerjoin(
            Listener,
            Listener.channel_id == Point.listener_channel_id,
        )
        .filter(
            True if not live_id else Live.live_id == live_id,
        )
        .filter(
            True if not liver_channel_id else Liver.channel_id == liver_channel_id,
        )
        .filter(
            True
            if not listener_channel_id
            else Point.listener_channel_id == listener_channel_id,
        )
        .group_by(Point.listener_channel_id, Listener.id)
        .order_by(func.sum(Point.value).desc())
        .limit(100)
        .all()
    )
    ret = []
    for value, lnr_cid, img, name in ranking:
        if not img or not name:
            comment = (
                db.query(Comment)
                .filter(
                    Comment.author_channel_id == lnr_cid,
                )
                .order_by(Comment.published_at.desc())
                .first()
            )
            img = img or comment.author_profile_image_url
            name = name or comment.display_name
        ret.append(
            {
                "point": value,
                "listener_channel_id": lnr_cid,
                "profile_image_url": img,
                "name": name,
            }
        )
    return {"ranking": ret}


def ranking_superchats(
    live_id,
    liver_channel_id,
    listener_channel_id,
    db,
):
    Liver = aliased(User)
    Listener = aliased(User)

    ranking = (
        db.query(
            func.sum(Comment.amount_micros),
            Comment.author_channel_id,
            Listener.profile_image_url,
            Listener.name,
        )
        .join(Live, Live.live_id == Comment.live_id)
        .join(Liver, Liver.id == Live.liver_id)
        .outerjoin(
            Listener,
            Listener.channel_id == Comment.author_channel_id,
        )
        .filter(
            Comment.type == "superChatEvent",
            Comment.currency == "JPY",
        )
        .filter(
            True if not live_id else Live.live_id == live_id,
        )
        .filter(
            True if not liver_channel_id else Liver.channel_id == liver_channel_id,
        )
        .filter(
            True
            if not listener_channel_id
            else Comment.author_channel_id == listener_channel_id,
        )
        .group_by(Comment.author_channel_id, Listener.id)
        .order_by(func.sum(Comment.amount_micros))
        .limit(100)
        .all()
    )
    ret = []
    for value, lnr_cid, img, name in ranking:
        if not img or not name:
            comment = (
                db.query(Comment)
                .filter(
                    Comment.author_channel_id == lnr_cid,
                )
                .order_by(Comment.published_at.desc())
                .first()
            )
            img = img or comment.author_profile_image_url
            name = name or comment.display_name
        ret.append(
            {
                "amount": value,
                "listener_channel_id": lnr_cid,
                "profile_image_url": img,
                "name": name,
            }
        )
    return {"ranking": ret}


def ranking_comments(
    live_id,
    liver_channel_id,
    listener_channel_id,
    db,
):
    Liver = aliased(User)
    Listener = aliased(User)

    ranking = (
        db.query(
            func.count(Comment.author_channel_id),
            Comment.author_channel_id,
            Listener.profile_image_url,
            Listener.name,
        )
        .join(Live, Live.live_id == Comment.live_id)
        .join(Liver, Liver.id == Live.liver_id)
        .outerjoin(
            Listener,
            Listener.channel_id == Comment.author_channel_id,
        )
        .filter(
            True if not live_id else Live.live_id == live_id,
        )
        .filter(
            True if not liver_channel_id else Liver.channel_id == liver_channel_id,
        )
        .filter(
            True
            if not listener_channel_id
            else Comment.author_channel_id == listener_channel_id,
        )
        .group_by(Comment.author_channel_id, Listener.id)
        .order_by(func.sum(Comment.author_channel_id))
        .limit(100)
        .all()
    )
    ret = []
    for value, lnr_cid, img, name in ranking:
        if not img or not name:
            comment = (
                db.query(Comment)
                .filter(
                    Comment.author_channel_id == lnr_cid,
                )
                .order_by(Comment.published_at.desc())
                .first()
            )
            img = img or comment.author_profile_image_url
            name = name or comment.display_name
        ret.append(
            {
                "count": value,
                "listener_channel_id": lnr_cid,
                "profile_image_url": img,
                "name": name,
            }
        )
    return {"ranking": ret}
