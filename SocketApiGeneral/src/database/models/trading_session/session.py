from datetime import datetime

import sqlalchemy as sqla
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy_utils import ChoiceType

from src.database.models.core import Timestamp

CHANNEL_TYPES = [
    ("vip", "vip"),
    ("public", "public"),
]


class TraderSession(Timestamp):
    __tablename__ = "trader_sessions"

    id: Mapped[int] = sqla.Column(
        sqla.Integer(),
        primary_key=True,
    )

    title: Mapped[str] = sqla.Column(
        sqla.String(),
        nullable=False,
    )

    start_datetime: Mapped[datetime] = sqla.Column(
        sqla.DateTime(),
        nullable=False,
    )

    is_active: Mapped[bool] = sqla.Column(
        sqla.Boolean(),
        default=True,
    )

    type: Mapped[str] = sqla.Column(
        ChoiceType(CHANNEL_TYPES),
        nullable=False,
    )

    responsible_trader_id: Mapped[int] = sqla.Column(
        sqla.Integer(),
        sqla.ForeignKey("traders.id"),
        nullable=False,
    )

    channel_id: Mapped[int] = sqla.Column(
        sqla.Integer(),
        sqla.ForeignKey("channels.id"),
        nullable=False,
    )

    responsible_trader = relationship("Trader", back_populates="trader_sessions")
    channel = relationship("Channel", back_populates="sessions")
    announcements = relationship(
        "TraderSessionAnnouncement", back_populates="session", cascade="all, delete"
    )
    session_messages = relationship(
        "TraderSessionMessage", back_populates="session", cascade="all, delete"
    )

    def __str__(self) -> str:
        return f"Session: {self.title}"


class TraderSessionMessage(Timestamp):
    __tablename__ = "trader_session_messages"

    id: Mapped[int] = sqla.Column(
        sqla.Integer(),
        primary_key=True,
    )

    text: Mapped[str] = sqla.Column(
        sqla.String(),
        nullable=False,
    )

    photo_id: Mapped[str] = sqla.Column(
        sqla.String(),
    )

    message_id: Mapped[int] = sqla.Column(
        sqla.Integer(),
        nullable=False,
    )

    session_id: Mapped[int] = sqla.Column(
        sqla.Integer(),
        sqla.ForeignKey("trader_sessions.id"),
        nullable=False,
    )

    session = relationship("TraderSession", back_populates="session_messages")
