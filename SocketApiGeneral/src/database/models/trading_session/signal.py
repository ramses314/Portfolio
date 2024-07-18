import sqlalchemy as sqla
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy_utils import ChoiceType

from src.database.models.core import Timestamp

MESSAGE_TYPES = [
    ("trade_up", "trade_up"),
    ("trade_down", "trade_down"),
    ("1_minute", "1_minute"),
    ("2_minute", "2_minute"),
    ("end_for_vip", "end_for_vip"),
    ("end_for_public", "end_for_public"),
    ("button_text", "button_text"),
]


class TraderSessionSignal(Timestamp):
    __tablename__ = "trader_session_signals"

    id: Mapped[int] = sqla.Column(
        sqla.Integer(),
        primary_key=True,
    )

    text: Mapped[str] = sqla.Column(
        sqla.String(),
        nullable=False,
    )

    message_type: Mapped[str] = sqla.Column(
        ChoiceType(MESSAGE_TYPES),
        nullable=False,
    )

    influencer_id: Mapped[int] = sqla.Column(
        sqla.Integer(),
        sqla.ForeignKey("influencers.id"),
        nullable=False,
    )

    influencer = relationship("Influencer", back_populates="signals")
