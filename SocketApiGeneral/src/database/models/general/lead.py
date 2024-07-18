from datetime import datetime, date

from sqlalchemy import (
    DECIMAL,
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    func, Text, TEXT,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base
from src.database.models.core import Timestamp
from src.database.models import *


lead_influencer_table = Table(
    "lead_influencer_association",
    Base.metadata,
    Column("lead_id", Integer, ForeignKey("leads.id"), primary_key=True),
    Column("influencer_id", Integer, ForeignKey("influencers.id"), primary_key=True),
)


class Lead(Timestamp):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(
        Integer(),
        primary_key=True,
    )
    username: Mapped[str] = mapped_column(
        String(50),
        nullable=True,
    )
    first_name: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )
    first_tourch: Mapped[str] = mapped_column(String(255), nullable=True)
    tg_id: Mapped[int] = mapped_column(
        BigInteger(),
        nullable=False,
    )
    radist_chat_id: Mapped[int] = mapped_column(
        BigInteger(),
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean(),
        default=True,
        nullable=True,
    )
    is_chat_delete: Mapped[bool] = mapped_column(
        Boolean(),
        default=False,
        nullable=True,
    )
    is_subscribe: Mapped[bool] = mapped_column(
        Boolean(),
        default=False,
        nullable=True,
    )
    is_wrote: Mapped[bool] = mapped_column(
        Boolean(),
        default=False,
        nullable=True,
    )

    crm_users: Mapped["CRMUser"] = relationship(
        "CRMUser",
        back_populates="leads",
        lazy="subquery",
    )
    crm_user_id: Mapped[int] = mapped_column(ForeignKey("crm_users.id"), nullable=True)

    crm_contacts: Mapped["CRMContact"] = relationship(
        "CRMContact",
        back_populates="leads",
        lazy="subquery",
    )

    crm_leads: Mapped["CRMLead"] = relationship(
        "CRMLead",
        back_populates="leads",
        lazy="subquery",
    )

    invites: Mapped[list["LeadInvite"]] = relationship(
        "LeadInvite",
        back_populates="lead",
        lazy="subquery",
    )

    influencers = relationship(
        "Influencer",
        secondary=lead_influencer_table,
        back_populates="leads",
        lazy="subquery"
    )

    bots: Mapped[list["LeadBot"]] = relationship(
        "LeadBot",
        back_populates="lead",
        lazy="subquery",
    )

    channels = relationship(
        "LeadChannel",
        back_populates="lead",
        lazy="subquery",
    )

    radist_messages = relationship(
        "MessageRadist",
        back_populates="lead",
        lazy="subquery",
    )

    messages = relationship(
        "LeadMessage",
        back_populates="lead",
        lazy="subquery",
    )

    keitars: Mapped[list["LeadKeitaro"]] = relationship(
        "LeadKeitaro",
        back_populates="lead",
        lazy="subquery",
    )

    steps: Mapped[list["LeadStep"]] = relationship(
        "LeadStep",
        back_populates="lead",
        lazy = "subquery",
    )

    lead_signals: Mapped[list["LeadSignal"]] = relationship("LeadSignal", back_populates="lead", lazy = "subquery")

    def __str__(self):
        return f"Lid {self.username} - {self.id}"


class LeadInvite(Timestamp):
    __tablename__ = "lead_invites"

    id: Mapped[int] = mapped_column(
        Integer(),
        primary_key=True,
    )
    company_name: Mapped[str] = mapped_column(
        String(),
        nullable=True,
    )
    buyer: Mapped[str] = mapped_column(
        String(),
        nullable=True,
    )
    kid: Mapped[str] = mapped_column(String(), nullable=True)

    utms: Mapped[list["LeadInviteUtm"]] = relationship(
        "LeadInviteUtm",
        back_populates="invites",
        lazy="subquery",
    )

    lead_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("leads.id"),
        nullable=True,
    )
    lead: Mapped["Lead"] = relationship(
        "Lead",
        back_populates="invites",
        lazy="subquery",
    )

    def __str__(self):
        return f"Lead invite - {self.id}"


class LeadInviteUtm(Timestamp):
    __tablename__ = "utm_lead_invites"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    title: Mapped[str] = mapped_column(String(), nullable=True)
    number: Mapped[int] = mapped_column(Integer(), nullable=True)
    invite_id: Mapped[int] = mapped_column(Integer, ForeignKey("lead_invites.id"))
    invites: Mapped["LeadInvite"] = relationship("LeadInvite", back_populates="utms", lazy = "subquery",)

    def __str__(self):
        return f"Lead invite utm - {self.id}"


class LeadBot(Timestamp):
    __tablename__ = "lead_bots"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    name: Mapped[str] = mapped_column(String(), nullable=False)
    username: Mapped[str] = mapped_column(String(), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
    is_active_for_lead: Mapped[bool] = mapped_column(Boolean, default=False)
    lead_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("leads.id"),
    )
    lead = relationship("Lead", back_populates="bots", lazy="subquery")

    def __str__(self):
        return f"Lead bot - {self.id}"


class LeadStep(Timestamp):
    __tablename__ = "lead_steps"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    title: Mapped[str] = mapped_column(String(), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
    started = mapped_column(DateTime, default=func.now())
    finished = mapped_column(DateTime, nullable=True)
    lead_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("leads.id"), nullable=False
    )
    lead: Mapped["Lead"] = relationship("Lead", back_populates="steps", lazy = "subquery",)

    def __str__(self):
        return f"Lead step - {self.id}"


class LeadChannel(Timestamp):
    __tablename__ = "lead_channels"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    link_id: Mapped[str] = mapped_column(String(), nullable=False)
    leaved_datetime = mapped_column(DateTime, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)

    lead_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("leads.id"),
        nullable=False,
    )
    lead: Mapped["Lead"] = relationship("Lead", back_populates="channels", lazy = "subquery")

    influencer_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("influencers.id"),
        nullable=False,
    )
    influencer: Mapped["Influencer"] = relationship(
        "Influencer", back_populates="lead_channel", lazy = "subquery"
    )

    def __str__(self):
        return f"Lead channel - {self.id}"


class PartnerPostback(Timestamp):
    __tablename__ = "postback_partners"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    partner_id: Mapped[int] = mapped_column(Integer(), nullable=False)
    tg_id: Mapped[int] = mapped_column(BigInteger(), nullable=True)
    status: Mapped[str] = mapped_column(String(), nullable=True)
    event_id: Mapped[str] = mapped_column(String(), nullable=True)
    payout: Mapped[float] = mapped_column(DECIMAL(), nullable=True)
    link_id: Mapped[int] = mapped_column(Integer())
    click_id: Mapped[str] = mapped_column(String(), nullable=True)

    crm_lead_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey("crm_leads.id"), nullable=True
    )
    crm_leads: Mapped["CRMLead"] = relationship("CRMLead", back_populates="partners", lazy = "subquery")

    rdeps = relationship("LeadPartnerRdep", back_populates="partner", lazy = "subquery")

    def __str__(self):
        return f"Partner postback - {self.id}"


class LeadMessage(Timestamp):
    __tablename__ = "lead_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    is_scam: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
    content: Mapped[str] = mapped_column(Text)

    lead_id: Mapped[int] = mapped_column(Integer, ForeignKey("leads.id"), nullable=True)
    lead: Mapped["Lead"] = relationship("Lead", back_populates="messages", lazy = "subquery")

    def __str__(self):
        return f"Lead message - {self.id}"


class LeadPartnerRdep(Timestamp):
    __tablename__ = "lead_partner_rdeps"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    deposit_sum: Mapped[float] = mapped_column(
        DECIMAL(precision=10, scale=2), default=0
    )

    partner_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("postback_partners.id"),
        nullable=False,
    )
    partner: Mapped["LeadPartnerRdep"] = relationship(
        "PartnerPostback", back_populates="rdeps", lazy = "subquery"
    )

    def __str__(self):
        return f"Lead partner RDEP - {self.id}"


class LeadSignal(Timestamp):
    __tablename__ = "lead_signals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    resubscribe: Mapped[int] = mapped_column(Integer, default=0)
    is_deposit: Mapped[bool] = mapped_column(Boolean, default=False)
    start_subscribe: Mapped[datetime | None]
    end_subscribe: Mapped[datetime | None]

    lead_id: Mapped[int] = mapped_column(Integer, ForeignKey("leads.id"))
    lead: Mapped["Lead"] = relationship("Lead", back_populates="lead_signals", lazy = "subquery",)


class News(Timestamp):
    __tablename__ = "news"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str] = mapped_column(TEXT, nullable=False)
    has_sent: Mapped[bool] = mapped_column(Boolean, default=False)

    def __str__(self):
        return f"News: {self.title}\n{self.created}"


class BotAdmin(Timestamp):
    __tablename__ = "bot_admins"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    username: Mapped[str] = mapped_column(String(255), default="404", nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
