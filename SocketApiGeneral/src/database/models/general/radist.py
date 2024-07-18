from sqlalchemy import (
    BigInteger,
    Boolean,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.models.core import Timestamp
from src.database.models import LeadSignal


class RadistInfluencer(Timestamp):
    __tablename__ = "radist_influencer"

    id: Mapped[int] = mapped_column(
        Integer(),
        primary_key=True,
    )
    connection_id: Mapped[Integer] = mapped_column(
        Integer(),
        nullable=False,
    )
    connection_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    radist_influencer_leads: Mapped["RadistInfluencerLeads"] = relationship(
        "RadistInfluencerLeads", back_populates="radist_influencer", lazy = "subquery"
    )
    influencer = relationship("Influencer", back_populates="radist_influencer", lazy = "subquery")
    influencer_id = mapped_column(Integer(), ForeignKey("influencers.id"))


class RadistInfluencerLeads(Timestamp):
    __tablename__ = "radist_influencer_leads"

    id: Mapped[int] = mapped_column(
        Integer(),
        primary_key=True,
    )
    contacts_id: Mapped[int] = mapped_column(
        Integer(),
        nullable=False,
    )
    radist_lead_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    radist_contact_chat_id: Mapped[int] = mapped_column(
        Integer(),
        nullable=False,
    )
    tg_id: Mapped[BigInteger] = mapped_column(
        BigInteger(),
        nullable=False,
    )

    radist_influencer_id = mapped_column(Integer(), ForeignKey("radist_influencer.id"))

    radist_influencer: Mapped[RadistInfluencer] = relationship(
        "RadistInfluencer", back_populates="radist_influencer_leads", lazy="subquery"
    )

    radist_messages: Mapped["MessageRadist"] = relationship(
        "MessageRadist", back_populates="radist_influencer_leads", lazy="subquery"
    )


class MessageRadist(Timestamp):
    __tablename__ = "message_radist"

    id: Mapped[int] = mapped_column(
        Integer(),
        primary_key=True,
    )
    radist_contact_chat_id: Mapped[int] = mapped_column(
        Integer(),
        nullable=False,
    )
    inbound_message: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )
    outbound_message: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )
    message: Mapped[Text] = mapped_column(
        Text(),
        nullable=False,
    )

    radist_influencer_lead_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey("radist_influencer_leads.id")
    )
    radist_influencer_leads = relationship(
        "RadistInfluencerLeads", back_populates="radist_messages", lazy="subquery"
    )

    lead: Mapped["RadistInfluencerLeads"] = relationship(
        "Lead", back_populates="radist_messages", lazy="subquery"
    )
    lead_id = mapped_column(Integer(), ForeignKey("leads.id"))
