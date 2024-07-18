from sqlalchemy import BigInteger, Boolean, Integer, String

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models import lead_influencer_table
from src.database.models.core import Timestamp


class Influencer(Timestamp):
    __tablename__ = "influencers"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    title: Mapped[str] = mapped_column(String(), nullable=False)
    tg_id: Mapped[int] = mapped_column(BigInteger(), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
    leads = relationship(
        "Lead", secondary=lead_influencer_table, back_populates="influencers", lazy="subquery"
    )
    channels = relationship(
        "Channel", back_populates="influencer", cascade="all, delete", lazy="subquery"
    )
    reminders = relationship(
        "TraderSessionReminder", back_populates="influencer", cascade="all, delete", lazy="subquery"
    )
    signals = relationship(
        "TraderSessionSignal", back_populates="influencer", cascade="all, delete", lazy="subquery"
    )
    lead_channel: Mapped["LeadChannel"] = relationship(
        "LeadChannel", back_populates="influencer", lazy="subquery"
    )
    radist_influencer = relationship(
        "RadistInfluencer", back_populates="influencer", uselist=False, lazy="subquery"
    )
    # lead_influencer_stories = relationship(
    #     "LeadInfluencerStory", back_populates="influencer"
    # )
    # personal_link: Mapped[str] = sqla.Column(
    #     sqla.String(),
    #     nullable=False,
    # )

    def __str__(self):
        return f"Influencer - {self.id}"
