from sqlalchemy import BigInteger, Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy_utils import ChoiceType

from src.database.models import Influencer
from src.database.models.core import Timestamp

CHANNEL_TYPES = [
    ("vip", "vip"),
    ("public", "public"),
]


class Channel(Timestamp):
    __tablename__ = "channels"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    channel_name: Mapped[str] = mapped_column(String(), nullable=False)
    chat_id: Mapped[int] = mapped_column(BigInteger(), nullable=False)
    subscribers: Mapped[int] = mapped_column(Integer(), default=0)
    is_private: Mapped[bool] = mapped_column(Boolean, default=True)
    type: Mapped[str] = mapped_column(
        ChoiceType(CHANNEL_TYPES)
    )

    influencer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("influencers.id"), nullable=False
    )
    influencer: Mapped["Influencer"] = relationship(
        "Influencer", back_populates="channels", lazy="subquery"
    )

    posts = relationship("ChannelPost", back_populates="channel", lazy = "subquery")
    sessions = relationship(
        "TraderSession", back_populates="channel", cascade="all, delete", lazy = "subquery"
    )

    def __str__(self):
        return f"Channel {self.channel_name} - {self.id}"


class ChannelPost(Timestamp):
    __tablename__ = "channel_posts"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    text: Mapped[str] = mapped_column(Text(), nullable=False)
    attached_content_type: Mapped[str] = mapped_column(String(), nullable=False)
    attachment_id: Mapped[str] = mapped_column(String(), nullable=False)
    reactions: Mapped[int] = mapped_column(Integer(), default=0)
    views: Mapped[int] = mapped_column(Integer(), default=0)
    post_id: Mapped[int] = mapped_column(Integer(), nullable=True)

    channel_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("channels.id"),
        nullable=True,
    )
    channel: Mapped["Channel"] = relationship("Channel", back_populates="posts", lazy = "subquery")

    def __str__(self):
        return f"Channel post - {self.id}"
