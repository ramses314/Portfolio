from .general.lead import (
    lead_influencer_table,
    Lead,
    LeadBot,
    LeadInvite,
    LeadInviteUtm,
    LeadStep,
    LeadChannel,
    PartnerPostback,
    LeadPartnerRdep,
    LeadSignal,
    BotAdmin,
    LeadMessage,
)
from .general.keitaro import LeadKeitaro
from .trading_session.session import TraderSession, TraderSessionMessage
from .trading_session.signal import TraderSessionSignal
from .trading_session.trader import (
    Trader,
    TraderSessionAnnouncement,
    TraderSessionReminder,
)

from .general.radist import RadistInfluencer, RadistInfluencerLeads, MessageRadist
from .general.radist import RadistInfluencer, MessageRadist
from .general.influencer import Influencer
from .general.channel import Channel, ChannelPost
from .general.amocrm import CRM, CRMUser, CRMContact, CRMLead

model_namespace = {
    "Channel": Channel,
    "ChannelPost": ChannelPost,
    "Lead": Lead,
    "LeadInvite": LeadInvite,
    "LeadBot": LeadBot,
    "LeadInviteUtm": LeadInviteUtm,
    "LeadChannel": LeadChannel,
    "LeadMessage": LeadMessage,
    "LeadStep": LeadStep,
    "LeadPartnerRdep": LeadPartnerRdep,
    "LeadKeitaro": LeadKeitaro,
    "CRMLead": CRMLead,
    "CRMUser": CRMUser,
    "CRMContact": CRMContact,
    "CRM": CRM,
    "Influencer": Influencer,
    "lead_influencer_table": lead_influencer_table,
    "PartnerPostback": PartnerPostback,
    "LeadSignal": LeadSignal,
    "TraderSession": TraderSession,
    "TraderSessionMessage": TraderSessionMessage,
    "TraderSessionSignal": TraderSessionSignal,
    "Trader": Trader,
    "TraderSessionAnnouncement": TraderSessionAnnouncement,
    "TraderSessionReminder": TraderSessionReminder,
    "RadistInfluencer": RadistInfluencer,
    "RadistInfluencerLeads": RadistInfluencerLeads,
    "MessageRadist": MessageRadist,
    "BotAdmin": BotAdmin,
}

related_field_id_mapper = {
    "amo_account_id": CRM,
    "crm_user_id": CRMUser,
    "lead_id": Lead,
    "influencer_id": Influencer,
    "channel_id": Channel,
    "responsible_trader_id": Trader,
    "radist_influencer_id": RadistInfluencer,
    "radist_influencer_lead_id": RadistInfluencerLeads,
    "partner_id": PartnerPostback,
}
