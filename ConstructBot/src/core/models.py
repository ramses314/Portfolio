import asyncio
import time

import sqlalchemy as sqla
import websockets
from sqlalchemy import event
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.types import DateTime, Interval
from datetime import datetime, timedelta

from src.core.database import Base, get_sync_session

utm_bot_person_association = sqla.Table(
    "bot_botperson_utms",
    Base.metadata,
    sqla.Column("utm_id", sqla.Integer(), sqla.ForeignKey("bot_utm.id"), primary_key=True),
    sqla.Column("botperson_id", sqla.Integer(), sqla.ForeignKey("bot_botperson.id"), primary_key=True),
)


class Lid(Base):
    __tablename__ = 'statistic_lid'
    __tablename__ = 'statistic_lid'

    id: Mapped[int] = sqla.Column(
        sqla.Integer(),
        primary_key=True
    )

    username: Mapped[str] = sqla.Column(
        sqla.String(255),
    )

    telegram_id: Mapped[int] = sqla.Column(
        sqla.BigInteger(),
        nullable=False
    )

    partner_pk: Mapped[str] = sqla.Column(
        sqla.String(),
        nullable=False,
    )

    current_step: Mapped[str] = sqla.Column(
        sqla.String(255),
        nullable=False,
    )

    private_link: Mapped[str] = sqla.Column(
        sqla.String(255)
    )

    datetime_startup: Mapped[datetime] = sqla.Column(
        sqla.DateTime,
        nullable=False,
        default=sqla.func.now()
    )

    datetime_stop: Mapped[datetime] = sqla.Column(
        sqla.DateTime,
    )

    is_channel_joined: Mapped[bool] = sqla.Column(
        sqla.Boolean(),
        default=False,
    )

    is_first_sender: Mapped[bool] = sqla.Column(
        sqla.Boolean(),
        default=False,
    )

    is_registered: Mapped[bool] = sqla.Column(
        sqla.Boolean(),
        default=False,
    )

    is_deposited: Mapped[bool] = sqla.Column(
        sqla.Boolean(),
        default=False,
    )

    is_finished: Mapped[bool] = sqla.Column(
        sqla.Boolean(),
        default=False,
    )

    is_active: Mapped[bool] = sqla.Column(
        sqla.Boolean(),
        default=True,
    )

    utm_id: Mapped[int] = sqla.Column(
        sqla.Integer(),
        sqla.ForeignKey("bot_utm.id"),
        nullable=False,
    )

    utm = relationship("Utm", back_populates="lids")
    stages = relationship("Stage", back_populates="lid")

    def to_dict(self):
        return {column.name: f"{getattr(self, column.name)}" for column in self.__table__.columns}

    def __str__(self):
        return f"lid №{self.id}"


class Utm(Base):
    __tablename__ = "bot_utm"

    id: Mapped[int] = sqla.Column(
        sqla.Integer(),
        primary_key=True,
    )

    title: Mapped[str] = sqla.Column(
        sqla.String(255),
        nullable=False,
    )

    funnel: Mapped[str] = sqla.Column(
        sqla.String(255),
        nullable=False,
    )

    link: Mapped[str] = sqla.Column(
        sqla.String(),
        nullable=False
    )

    public_chat_id = sqla.Column(
        sqla.BigInteger(),
    )

    private_chat_id = sqla.Column(
        sqla.BigInteger(),
    )

    is_delete_all: Mapped[bool] = sqla.Column(
        sqla.Boolean(),
        default=False,
    )

    is_delete_keyboard: Mapped[bool] = sqla.Column(
        sqla.Boolean(),
        default=False,
    )

    is_bot_person: Mapped[bool] = sqla.Column(
        sqla.Boolean(),
        default=False,
    )

    is_antiscam: Mapped[bool] = sqla.Column(
        sqla.Boolean(),
        default=False,
    )

    lids = relationship("Lid", back_populates="utm")
    steps = relationship("Step", back_populates="utm")
    bots_antiscam = relationship("BotAntiscam", back_populates="utm")
    confirmation_requests = relationship("ConfirmationRequest", back_populates="utm")
    bots_person = relationship("BotPerson", secondary=utm_bot_person_association, back_populates="utms")
    links_settings = relationship("LinkSettings", back_populates="utm")

    def __str__(self):
        return f"utm - {self.title}"


class Step(Base):
    __tablename__ = 'bot_step'

    id: Mapped[int] = sqla.Column(
        sqla.Integer(),
        primary_key=True,
    )

    title: Mapped[str] = sqla.Column(
        sqla.String(255),
        nullable=False,
    )

    title_info: Mapped[str] = sqla.Column(
        sqla.String(255),
        nullable=False,
    )

    reminder: Mapped[str] = sqla.Column(
        sqla.String(255),
    )

    send_after_min: Mapped[int] = sqla.Column(
        sqla.Integer(),
    )

    is_autorequest: Mapped[bool] = sqla.Column(
        sqla.Boolean(),
        default=False,
    )

    is_check_free_channel: Mapped[bool] = sqla.Column(
        sqla.Boolean(),
        default=False,
    )

    is_check_user_wrote: Mapped[bool] = sqla.Column(
        sqla.Boolean(),
        default=False,
    )

    is_photos_group: Mapped[bool] = sqla.Column(
        sqla.Boolean(),
        default=True,
    )

    is_videos_group: Mapped[bool] = sqla.Column(
        sqla.Boolean(),
        default=True,
    )

    construct: Mapped[list] = sqla.Column(
        sqla.ARRAY(sqla.String),
        nullable=False,
    )

    video_notes: Mapped[list] = sqla.Column(
        sqla.ARRAY(sqla.String),
    )

    videos: Mapped[list] = sqla.Column(
        sqla.ARRAY(sqla.String),
    )

    photos: Mapped[list] = sqla.Column(
        sqla.ARRAY(sqla.String),
    )

    texts: Mapped[list] = sqla.Column(
        sqla.ARRAY(sqla.String),
    )

    keyboards: Mapped[list] = sqla.Column(
        sqla.ARRAY(sqla.JSON),
    )

    utm_id: Mapped[int] = sqla.Column(
        sqla.Integer(),
        sqla.ForeignKey("bot_utm.id"),
        nullable=False
    )

    utm = relationship("Utm", back_populates="steps")

    def __str__(self):
        return f"step : {self.id}"


class LinkSettings(Base):
    __tablename__ = "bot_linksettings"

    id: Mapped[int] = sqla.Column(
        sqla.Integer(),
        primary_key=True,
    )

    title: Mapped[str] = sqla.Column(
        sqla.String(255),
        nullable=False
    )

    chat_id: Mapped[int] = sqla.Column(
        sqla.BigInteger(),
        nullable=False
    )

    expire_datetime: Mapped[datetime] = sqla.Column(
        DateTime(),
    )

    member_limit: Mapped[int] = sqla.Column(
        sqla.Integer(),
    )

    is_create_join_request: Mapped[bool] = sqla.Column(
        sqla.Boolean(),
        default=False
    )

    utm_id: Mapped[int] = sqla.Column(
        sqla.Integer(),
        sqla.ForeignKey("bot_utm.id"),
        nullable=False
    )

    utm = relationship("Utm", back_populates="links_settings")

    def __str__(self):
        return self.title


class Stage(Base):
    __tablename__ = "bot_stage"

    id: Mapped[int] = sqla.Column(
        sqla.Integer(),
        primary_key=True,
    )

    title: Mapped[str] = sqla.Column(
        sqla.String(100),
        nullable=False
    )

    created: Mapped[datetime] = sqla.Column(
        DateTime(timezone=True),
        default=sqla.func.now()
    )

    updated: Mapped[datetime] = sqla.Column(
        DateTime(timezone=True),
        default=sqla.func.now(),
        onupdate=sqla.func.now(),
    )

    finished: Mapped[datetime] = sqla.Column(
        DateTime(timezone=True),
    )

    activity_time: Mapped[timedelta] = sqla.Column(
        Interval,
    )

    lid_id: Mapped[int] = sqla.Column(
        sqla.Integer(),
        sqla.ForeignKey("statistic_lid.id"),
        nullable=False
    )

    lid = relationship("Lid", back_populates="stages")

    def to_dict(self):
        return {column.name: f"{getattr(self, column.name)}" for column in self.__table__.columns}


class BotAntiscam(Base):
    __tablename__ = "bot_botantiscam"

    id: Mapped[int] = sqla.Column(
        sqla.Integer(),
        primary_key=True,
    )

    token: Mapped[str] = sqla.Column(
        sqla.String(),
    )

    chat_id: Mapped[int] = sqla.Column(
        sqla.BigInteger(),
        nullable=False
    )

    utm_id: Mapped[int] = sqla.Column(
        sqla.Integer(),
        sqla.ForeignKey("bot_utm.id"),
        nullable=False
    )

    utm = relationship("Utm", back_populates="bots_antiscam")
    antiscam_messages = relationship("MessageAntiscam", back_populates="bot_antiscam")


class MessageAntiscam(Base):
    __tablename__ = "bot_messageantiscam"

    id: Mapped[int] = sqla.Column(
        sqla.Integer(),
        primary_key=True,
    )

    content: Mapped[str] = sqla.Column(
        sqla.String(),
        nullable=False
    )

    sender: Mapped[str] = sqla.Column(
        sqla.String(),
        nullable=False
    )

    recipient: Mapped[str] = sqla.Column(
        sqla.String(),
        nullable=False
    )

    inspector: Mapped[str] = sqla.Column(
        sqla.String(),
        nullable=False
    )

    partner_pk: Mapped[str] = sqla.Column(
        sqla.String(),
        nullable=False
    )

    bot_antiscam_id: Mapped[int] = sqla.Column(
        sqla.Integer(),
        sqla.ForeignKey("bot_botantiscam.id"),
        nullable=False,
    )

    bot_antiscam = relationship("BotAntiscam", back_populates="antiscam_messages")


class ConfirmationRequest(Base):
    __tablename__ = "bot_confirmationrequest"

    id: Mapped[int] = sqla.Column(
        sqla.Integer(),
        primary_key=True,
    )

    chat_id: Mapped[int] = sqla.Column(
        sqla.BigInteger(),
        unique=True,
        nullable=False
    )

    is_requested: Mapped[bool] = sqla.Column(
        sqla.Boolean(),
        default=False
    )

    utm_id: Mapped[int] = sqla.Column(
        sqla.Integer(),
        sqla.ForeignKey("bot_utm.id"),
        nullable=False
    )

    utm = relationship("Utm", back_populates="confirmation_requests")


class BotPerson(Base):
    __tablename__ = "bot_botperson"

    id: Mapped[int] = sqla.Column(
        sqla.Integer(),
        primary_key=True,
    )

    name: Mapped[str] = sqla.Column(
        sqla.String(150),
        nullable=False
    )

    api_id: Mapped[str] = sqla.Column(
        sqla.String(150),
        unique=True,
        nullable=False
    )

    hash: Mapped[str] = sqla.Column(
        sqla.String(150),
        unique=True,
        nullable=False,
    )

    phone: Mapped[str] = sqla.Column(
        sqla.String(100),
        nullable=False
    )

    session: Mapped[str] = sqla.Column(
        sqla.String(100),
    )

    utms = relationship("Utm", secondary=utm_bot_person_association, back_populates="bots_person")


# async def send_data_to_websocket(data):
#     try:
#         async with websockets.connect("ws://172.19.0.6/ws/connect") as websocket:
#             await websocket.send(data)
#             time.sleep(2)
#     except:
#         pass


@event.listens_for(Lid, "after_insert")
def lid_create_update(target, connection, obj, *args, **kw):
    to_send = {
        "from": "bot",
        "update": "lid",
        "data": obj.to_dict(),
    }
    # asyncio.create_task(send_data_to_websocket(str(to_send)))


@event.listens_for(Lid, "after_update")
def lid_create_update(target, connection, obj, *args, **kw):
    session = get_sync_session()
    lid = session.query(Lid).filter(Lid.id == obj.id).first()
    to_send = {
        "from": "bot",
        "update": "lid",
        "data": lid.to_dict(),
    }
    # asyncio.create_task(send_data_to_websocket(str(to_send)))
