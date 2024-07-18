from sqlalchemy import (
    DECIMAL,
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.models.core import Timestamp
from src.database.models import Lead


class CRM(Timestamp):
    __tablename__ = "crms"

    id: Mapped[int] = mapped_column(
        Integer(),
        primary_key=True,
    )
    link_crm: Mapped[str] = mapped_column(String(50), nullable=False)
    account_id_amo: Mapped[int] = mapped_column(Integer(), nullable=False)
    crm_users = relationship("CRMUser", back_populates="amo_accounts", lazy = "subquery")
    crm_contacts = relationship("CRMContact", back_populates="amo_accounts", lazy = "subquery")
    crm_leads = relationship("CRMLead", back_populates="amo_accounts", lazy = "subquery")

    def __str__(self):
        return f"CRM - {self.id}"


class CRMUser(Timestamp):
    __tablename__ = "crm_users"
    id: Mapped[int] = mapped_column(
        Integer(),
        primary_key=True,
    )

    amo_user_id: Mapped[int] = mapped_column(Integer(), nullable=False)
    username: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[str] = mapped_column(String(50), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True, nullable=False)
    full_access: Mapped[bool] = mapped_column(Boolean(), default=False)

    amo_account_id: Mapped[int] = mapped_column(
        ForeignKey("crms.id"), nullable=False
    )
    amo_accounts = relationship("CRM", back_populates="crm_users", lazy = "subquery")
    crm_leads: Mapped["CRMLead"] = relationship("CRMLead", back_populates="crm_users", lazy = "subquery")
    crm_contacts: Mapped["CRMContact"] = relationship("CRMContact", back_populates="crm_users", lazy = "subquery")
    leads = relationship("Lead", back_populates="crm_users", lazy = "subquery")

    def __str__(self):
        return f"CRM user - {self.id}"


class CRMContact(Timestamp):
    __tablename__ = "crm_contacts"
    id: Mapped[int] = mapped_column(
        Integer(),
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(String(50), nullable=True)
    contact_id: Mapped[int] = mapped_column(Integer(), nullable=False)

    amo_account_id: Mapped[int] = mapped_column(ForeignKey("crms.id"), nullable=False)
    amo_accounts = relationship("CRM", back_populates="crm_contacts", lazy="subquery")

    crm_user_id: Mapped[str] = mapped_column(ForeignKey("crm_users.id"))
    crm_users = relationship("CRMUser", back_populates="crm_contacts", lazy="subquery")

    lead_id: Mapped[int] = mapped_column(Integer(), ForeignKey("leads.id"))
    leads: Mapped["CRMLead"] = relationship("Lead", back_populates="crm_contacts", lazy="subquery")

    def __str__(self):
        return f"CRM contact - {self.id}"


class CRMLead(Timestamp):
    __tablename__ = "crm_leads"
    id: Mapped[int] = mapped_column(
        Integer(),
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(String(50))
    crm_lead_id: Mapped[int] = mapped_column(Integer())  # внутренний lead_id для amo
    status_id: Mapped[int] = mapped_column(Integer())
    pipeline_id: Mapped[int] = mapped_column(Integer())
    pipeline_name: Mapped[str] = mapped_column(String())
    telegram_id: Mapped[BigInteger] = mapped_column(BigInteger(), nullable=True)
    quotex_id: Mapped[int] = mapped_column(Integer(), nullable=True)
    dep_count: Mapped[int] = mapped_column(Integer(), nullable=True)
    dep_sum: Mapped[int] = mapped_column(Integer())

    reg_datetime: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    ftd_datetime: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    ftd_amount: Mapped[float] = mapped_column(DECIMAL(), nullable=True)
    last_dep: Mapped[DateTime] = mapped_column(DateTime, nullable=True)

    reg_event: Mapped[bool] = mapped_column(Boolean(), default=False)
    ftd_event: Mapped[bool] = mapped_column(Boolean(), default=False)

    amo_account_id: Mapped[int] = mapped_column(Integer, ForeignKey("crms.id"))
    amo_accounts = relationship("CRM", back_populates="crm_leads", lazy="subquery")

    lead_id: Mapped[int] = mapped_column(Integer, ForeignKey("leads.id"))
    leads = relationship("Lead", back_populates="crm_leads", lazy="subquery")

    crm_user_id: Mapped[int] = mapped_column(Integer, ForeignKey("crm_users.id"))
    crm_users = relationship("CRMUser", back_populates="crm_leads", lazy="subquery")

    partners = relationship("PartnerPostback", back_populates="crm_leads", lazy="subquery")

    def __str__(self):
        return f"CRM lead - {self.id}"
