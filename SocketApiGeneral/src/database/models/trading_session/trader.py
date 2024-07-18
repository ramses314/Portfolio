from datetime import timedelta

import sqlalchemy as sqla
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy_utils import ChoiceType

from src.database.models.core import Timestamp

CHANNEL_TYPES = [
    ("vip", "vip"),
    ("public", "public"),
]


class Trader(Timestamp):
    __tablename__ = "traders"

    id: Mapped[int] = sqla.Column(sqla.Integer(), primary_key=True)

    is_active: Mapped[bool] = sqla.Column(
        sqla.Boolean(),
        default=True,
    )

    telegram_id: Mapped[int] = sqla.Column(
        sqla.BigInteger(),
        nullable=False,
    )

    trader_sessions = relationship(
        "TraderSession", back_populates="responsible_trader", cascade="all, delete"
    )

    def __str__(self):
        return f"User id: {self.telegram_id}"


class TraderSessionReminder(Timestamp):
    __tablename__ = "trader_session_reminders"

    id: Mapped[int] = sqla.Column(
        sqla.Integer(),
        primary_key=True,
    )

    text: Mapped[str] = sqla.Column(
        sqla.String(),
        nullable=False,
    )

    remind_interval: Mapped[timedelta] = sqla.Column(
        sqla.Interval(),
        nullable=False,
    )

    type: Mapped[str] = sqla.Column(
        ChoiceType(CHANNEL_TYPES),
        nullable=False,
    )

    influencer_id: Mapped[int] = sqla.Column(
        sqla.Integer(),
        sqla.ForeignKey("influencers.id"),
        nullable=False,
    )

    influencer = relationship("Influencer", back_populates="reminders")


class TraderSessionAnnouncement(Timestamp):
    __tablename__ = "trader_session_announcements"

    id: Mapped[int] = sqla.Column(
        sqla.Integer(),
        primary_key=True,
    )

    title: Mapped[str] = sqla.Column(
        sqla.String(),
        nullable=False,
    )

    text: Mapped[str] = sqla.Column(
        sqla.String(),
        nullable=False,
    )

    is_active: Mapped[bool] = sqla.Column(
        sqla.Boolean(),
        default=True,
    )

    remind_interval: Mapped[timedelta] = sqla.Column(
        sqla.Interval(),
        nullable=False,
    )

    session_id: Mapped[int] = sqla.Column(
        sqla.Integer(),
        sqla.ForeignKey("trader_sessions.id"),
        nullable=False,
    )

    session = relationship("TraderSession", back_populates="announcements")
