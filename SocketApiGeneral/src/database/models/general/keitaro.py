from sqlalchemy import (
    JSON,
    Boolean,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models import Lead
from src.database.models.core import Timestamp


class LeadKeitaro(Timestamp):
    __tablename__ = "lead_keitaro"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source: Mapped[str] = mapped_column(String(255), nullable=True)
    x_requested_with: Mapped[str] = mapped_column(String(255), nullable=True)
    referrer: Mapped[str] = mapped_column(String(255), nullable=True)
    search_engine: Mapped[str] = mapped_column(String(255), nullable=True)
    keyword: Mapped[str] = mapped_column(String(255), nullable=True)
    click_id: Mapped[str] = mapped_column(String(255), nullable=True)
    sub_id: Mapped[str] = mapped_column(String(255))
    visitor_code: Mapped[str] = mapped_column(String(255), nullable=True)
    campaign_id: Mapped[int] = mapped_column(Integer, nullable=True)
    landing_id: Mapped[int] = mapped_column(Integer, nullable=True)
    offer_id: Mapped[int] = mapped_column(Integer, nullable=True)
    affiliate_network_id: Mapped[int] = mapped_column(Integer, nullable=True)
    ts_id: Mapped[int] = mapped_column(Integer, nullable=True)
    stream_id: Mapped[int] = mapped_column(Integer, nullable=True)
    ad_campaign_id: Mapped[str] = mapped_column(String(255), nullable=True)
    external_id: Mapped[str] = mapped_column(String(255), nullable=True)
    creative_id: Mapped[str] = mapped_column(String(255), nullable=True)

    sub_id_1: Mapped[str] = mapped_column(String(255), nullable=True)
    sub_id_2: Mapped[str] = mapped_column(String(255), nullable=True)
    sub_id_3: Mapped[str] = mapped_column(String(255), nullable=True)
    sub_id_4: Mapped[str] = mapped_column(String(255), nullable=True)
    sub_id_5: Mapped[str] = mapped_column(String(255), nullable=True)
    sub_id_6: Mapped[str] = mapped_column(String(255), nullable=True)
    sub_id_7: Mapped[str] = mapped_column(String(255), nullable=True)
    sub_id_8: Mapped[str] = mapped_column(String(255), nullable=True)
    sub_id_9: Mapped[str] = mapped_column(String(255), nullable=True)
    sub_id_10: Mapped[str] = mapped_column(String(255), nullable=True)
    sub_id_11: Mapped[str] = mapped_column(String(255), nullable=True)
    sub_id_12: Mapped[str] = mapped_column(String(255), nullable=True)
    sub_id_13: Mapped[str] = mapped_column(String(255), nullable=True)
    sub_id_14: Mapped[str] = mapped_column(String(255), nullable=True)
    sub_id_15: Mapped[str] = mapped_column(String(255), nullable=True)

    connection_type: Mapped[str] = mapped_column(String(255), nullable=True)
    operator: Mapped[str] = mapped_column(String(2255), nullable=True)
    isp: Mapped[str] = mapped_column(String(255), nullable=True)
    country_flag: Mapped[str] = mapped_column(String(255), nullable=True)
    country: Mapped[str] = mapped_column(String(255), nullable=True)
    region: Mapped[str] = mapped_column(String(255), nullable=True)
    city: Mapped[str] = mapped_column(String(255), nullable=True)
    language: Mapped[str] = mapped_column(String(255), nullable=True)
    device_type: Mapped[str] = mapped_column(String(255), nullable=True)
    user_agent: Mapped[str] = mapped_column(String(255), nullable=True)
    os_icon: Mapped[str] = mapped_column(String(255), nullable=True)
    os: Mapped[str] = mapped_column(String(255), nullable=True)
    os_version: Mapped[str] = mapped_column(String(255), nullable=True)
    browser: Mapped[str] = mapped_column(String(255), nullable=True)
    browser_version: Mapped[str] = mapped_column(String(255), nullable=True)

    device_model: Mapped[str] = mapped_column(String(255), nullable=True)
    browser_icon: Mapped[str] = mapped_column(String(255), nullable=True)
    ip: Mapped[str] = mapped_column(String(255), nullable=True)
    ip_mask1: Mapped[str] = mapped_column(String(255), nullable=True)
    ip_mask2: Mapped[str] = mapped_column(String(255), nullable=True)
    datetime: Mapped[str] = mapped_column(String(255), nullable=True)
    day_hour: Mapped[str] = mapped_column(String(255), nullable=True)
    landing_clicked_datetime: Mapped[str] = mapped_column(String(255), nullable=True)
    destination: Mapped[str] = mapped_column(String(255), nullable=True)
    is_unique_stream: Mapped[bool] = mapped_column(Boolean(), default=False)
    is_unique_campaign: Mapped[bool] = mapped_column(Boolean(), default=False)
    is_unique_global: Mapped[bool] = mapped_column(Boolean(), default=False)
    is_bot: Mapped[bool] = mapped_column(Boolean(), default=False)
    is_empty_referrer: Mapped[bool] = mapped_column(Boolean(), default=False)
    is_using_proxy: Mapped[bool] = mapped_column(Boolean(), default=False)
    landing_clicked: Mapped[bool] = mapped_column(Boolean(), default=False)
    is_lead: Mapped[bool] = mapped_column(Boolean(), default=False)
    is_sale: Mapped[bool] = mapped_column(Boolean(), default=False)
    is_rejected: Mapped[bool] = mapped_column(Boolean(), default=False)
    parent_campaign_id: Mapped[int] = mapped_column(Integer, nullable=True)
    parent_sub_ids: Mapped[JSON] = mapped_column(JSON, nullable=True)
    cost: Mapped[int] = mapped_column(Integer(), nullable=True)
    profitability: Mapped[int] = mapped_column(Integer(), nullable=True)
    revenue: Mapped[int] = mapped_column(Integer(), nullable=True)
    profit: Mapped[int] = mapped_column(Integer(), nullable=True)
    lead_revenue: Mapped[int] = mapped_column(Integer(), nullable=True)
    sale_revenue: Mapped[int] = mapped_column(Integer(), nullable=True)
    rejected_revenue: Mapped[int] = mapped_column(Integer(), nullable=True)
    rebills: Mapped[int] = mapped_column(Integer(), nullable=True)
    landing_clicked_period: Mapped[int] = mapped_column(Integer(), nullable=True)
    campaign: Mapped[str] = mapped_column(String(), nullable=True)
    campaign_group: Mapped[str] = mapped_column(String(), nullable=True)
    offer: Mapped[str] = mapped_column(String(), nullable=True)
    offer_group: Mapped[str] = mapped_column(String(), nullable=True)
    stream: Mapped[str] = mapped_column(String(), nullable=True)
    landing: Mapped[str] = mapped_column(String(), nullable=True)
    ts: Mapped[str] = mapped_column(String(), nullable=True)
    affiliate_network: Mapped[str] = mapped_column(String(), nullable=True)
 
    lead_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("leads.id"),
        nullable=True,
    )
    lead: Mapped["Lead"] = relationship("Lead", back_populates="keitars", lazy = "subquery")
    
    def __str__(self):
        return f"Keitaro - {self.id}"
