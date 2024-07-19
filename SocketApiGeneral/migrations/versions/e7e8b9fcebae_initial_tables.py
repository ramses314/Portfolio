"""Initial tables

Revision ID: e7e8b9fcebae
Revises:
Create Date: 2024-05-22 15:09:36.908586

"""
from typing import Sequence, Union
import sqlalchemy_utils
from src.database.models.general.channel import CHANNEL_TYPES
from src.database.models.trading_session.signal import MESSAGE_TYPES
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e7e8b9fcebae'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bot_admins',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tg_id', sa.BigInteger(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('crms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('link_crm', sa.String(length=50), nullable=False),
    sa.Column('account_id_amo', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('influencers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('tg_id', sa.BigInteger(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('news',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('body', sa.TEXT(), nullable=False),
    sa.Column('has_sent', sa.Boolean(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('traders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('telegram_id', sa.BigInteger(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('channels',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('channel_name', sa.String(), nullable=False),
    sa.Column('chat_id', sa.BigInteger(), nullable=False),
    sa.Column('subscribers', sa.Integer(), nullable=False),
    sa.Column('is_private', sa.Boolean(), nullable=False),
    sa.Column('type', sqlalchemy_utils.types.choice.ChoiceType(CHANNEL_TYPES), nullable=False),
    sa.Column('influencer_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['influencer_id'], ['influencers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('crm_users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('amo_user_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=50), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('full_access', sa.Boolean(), nullable=False),
    sa.Column('amo_account_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['amo_account_id'], ['crms.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('radist_influencer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('connection_id', sa.Integer(), nullable=False),
    sa.Column('connection_name', sa.String(length=50), nullable=False),
    sa.Column('influencer_id', sa.Integer(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['influencer_id'], ['influencers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('trader_session_reminders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('remind_interval', sa.Interval(), nullable=False),
    sa.Column('type', sqlalchemy_utils.types.choice.ChoiceType(CHANNEL_TYPES), nullable=False),
    sa.Column('influencer_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['influencer_id'], ['influencers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('trader_session_signals',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('message_type', sqlalchemy_utils.types.choice.ChoiceType(MESSAGE_TYPES), nullable=False),
    sa.Column('influencer_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['influencer_id'], ['influencers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('channel_posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('attached_content_type', sa.String(), nullable=False),
    sa.Column('attachment_id', sa.String(), nullable=False),
    sa.Column('reactions', sa.Integer(), nullable=False),
    sa.Column('views', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('channel_id', sa.Integer(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['channel_id'], ['channels.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('leads',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('first_name', sa.String(length=255), nullable=True),
    sa.Column('first_tourch', sa.String(length=255), nullable=True),
    sa.Column('tg_id', sa.BigInteger(), nullable=False),
    sa.Column('radist_chat_id', sa.BigInteger(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_chat_delete', sa.Boolean(), nullable=True),
    sa.Column('is_subscribe', sa.Boolean(), nullable=True),
    sa.Column('is_wrote', sa.Boolean(), nullable=True),
    sa.Column('crm_user_id', sa.Integer(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['crm_user_id'], ['crm_users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('radist_influencer_leads',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('contacts_id', sa.Integer(), nullable=False),
    sa.Column('radist_lead_name', sa.String(length=50), nullable=False),
    sa.Column('radist_contact_chat_id', sa.Integer(), nullable=False),
    sa.Column('tg_id', sa.BigInteger(), nullable=False),
    sa.Column('radist_influencer_id', sa.Integer(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['radist_influencer_id'], ['radist_influencer.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('trader_sessions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('start_datetime', sa.DateTime(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('type', sqlalchemy_utils.types.choice.ChoiceType(CHANNEL_TYPES), nullable=False),
    sa.Column('responsible_trader_id', sa.Integer(), nullable=False),
    sa.Column('channel_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['channel_id'], ['channels.id'], ),
    sa.ForeignKeyConstraint(['responsible_trader_id'], ['traders.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('crm_contacts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('contact_id', sa.Integer(), nullable=False),
    sa.Column('amo_account_id', sa.Integer(), nullable=False),
    sa.Column('crm_user_id', sa.Integer(), nullable=False),
    sa.Column('lead_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['amo_account_id'], ['crms.id'], ),
    sa.ForeignKeyConstraint(['crm_user_id'], ['crm_users.id'], ),
    sa.ForeignKeyConstraint(['lead_id'], ['leads.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('crm_leads',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('crm_lead_id', sa.Integer(), nullable=False),
    sa.Column('status_id', sa.Integer(), nullable=False),
    sa.Column('pipeline_id', sa.Integer(), nullable=False),
    sa.Column('pipeline_name', sa.String(), nullable=False),
    sa.Column('telegram_id', sa.BigInteger(), nullable=True),
    sa.Column('quotex_id', sa.Integer(), nullable=True),
    sa.Column('dep_count', sa.Integer(), nullable=True),
    sa.Column('dep_sum', sa.Integer(), nullable=False),
    sa.Column('reg_datetime', sa.DateTime(), nullable=True),
    sa.Column('ftd_datetime', sa.DateTime(), nullable=True),
    sa.Column('ftd_amount', sa.DECIMAL(), nullable=True),
    sa.Column('last_dep', sa.DateTime(), nullable=True),
    sa.Column('reg_event', sa.Boolean(), nullable=False),
    sa.Column('ftd_event', sa.Boolean(), nullable=False),
    sa.Column('amo_account_id', sa.Integer(), nullable=False),
    sa.Column('lead_id', sa.Integer(), nullable=False),
    sa.Column('crm_user_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['amo_account_id'], ['crms.id'], ),
    sa.ForeignKeyConstraint(['crm_user_id'], ['crm_users.id'], ),
    sa.ForeignKeyConstraint(['lead_id'], ['leads.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('lead_bots',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_active_for_lead', sa.Boolean(), nullable=False),
    sa.Column('lead_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['lead_id'], ['leads.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('lead_channels',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('link_id', sa.String(), nullable=False),
    sa.Column('leaved_datetime', sa.DateTime(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('lead_id', sa.Integer(), nullable=False),
    sa.Column('influencer_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['influencer_id'], ['influencers.id'], ),
    sa.ForeignKeyConstraint(['lead_id'], ['leads.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('lead_influencer_association',
    sa.Column('lead_id', sa.Integer(), nullable=False),
    sa.Column('influencer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['influencer_id'], ['influencers.id'], ),
    sa.ForeignKeyConstraint(['lead_id'], ['leads.id'], ),
    sa.PrimaryKeyConstraint('lead_id', 'influencer_id')
    )
    op.create_table('lead_invites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_name', sa.String(), nullable=True),
    sa.Column('buyer', sa.String(), nullable=True),
    sa.Column('kid', sa.String(), nullable=True),
    sa.Column('lead_id', sa.Integer(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['lead_id'], ['leads.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('lead_keitaro',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('source', sa.String(length=255), nullable=True),
    sa.Column('x_requested_with', sa.String(length=255), nullable=True),
    sa.Column('referrer', sa.String(length=255), nullable=True),
    sa.Column('search_engine', sa.String(length=255), nullable=True),
    sa.Column('keyword', sa.String(length=255), nullable=True),
    sa.Column('click_id', sa.String(length=255), nullable=True),
    sa.Column('sub_id', sa.String(length=255), nullable=False),
    sa.Column('visitor_code', sa.String(length=255), nullable=True),
    sa.Column('campaign_id', sa.Integer(), nullable=True),
    sa.Column('landing_id', sa.Integer(), nullable=True),
    sa.Column('offer_id', sa.Integer(), nullable=True),
    sa.Column('affiliate_network_id', sa.Integer(), nullable=True),
    sa.Column('ts_id', sa.Integer(), nullable=True),
    sa.Column('stream_id', sa.Integer(), nullable=True),
    sa.Column('ad_campaign_id', sa.String(length=255), nullable=True),
    sa.Column('external_id', sa.String(length=255), nullable=True),
    sa.Column('creative_id', sa.String(length=255), nullable=True),
    sa.Column('sub_id_1', sa.String(length=255), nullable=True),
    sa.Column('sub_id_2', sa.String(length=255), nullable=True),
    sa.Column('sub_id_3', sa.String(length=255), nullable=True),
    sa.Column('sub_id_4', sa.String(length=255), nullable=True),
    sa.Column('sub_id_5', sa.String(length=255), nullable=True),
    sa.Column('sub_id_6', sa.String(length=255), nullable=True),
    sa.Column('sub_id_7', sa.String(length=255), nullable=True),
    sa.Column('sub_id_8', sa.String(length=255), nullable=True),
    sa.Column('sub_id_9', sa.String(length=255), nullable=True),
    sa.Column('sub_id_10', sa.String(length=255), nullable=True),
    sa.Column('sub_id_11', sa.String(length=255), nullable=True),
    sa.Column('sub_id_12', sa.String(length=255), nullable=True),
    sa.Column('sub_id_13', sa.String(length=255), nullable=True),
    sa.Column('sub_id_14', sa.String(length=255), nullable=True),
    sa.Column('sub_id_15', sa.String(length=255), nullable=True),
    sa.Column('connection_type', sa.String(length=255), nullable=True),
    sa.Column('operator', sa.String(length=2255), nullable=True),
    sa.Column('isp', sa.String(length=255), nullable=True),
    sa.Column('country_flag', sa.String(length=255), nullable=True),
    sa.Column('country', sa.String(length=255), nullable=True),
    sa.Column('region', sa.String(length=255), nullable=True),
    sa.Column('city', sa.String(length=255), nullable=True),
    sa.Column('language', sa.String(length=255), nullable=True),
    sa.Column('device_type', sa.String(length=255), nullable=True),
    sa.Column('user_agent', sa.String(length=255), nullable=True),
    sa.Column('os_icon', sa.String(length=255), nullable=True),
    sa.Column('os', sa.String(length=255), nullable=True),
    sa.Column('os_version', sa.String(length=255), nullable=True),
    sa.Column('browser', sa.String(length=255), nullable=True),
    sa.Column('browser_version', sa.String(length=255), nullable=True),
    sa.Column('device_model', sa.String(length=255), nullable=True),
    sa.Column('browser_icon', sa.String(length=255), nullable=True),
    sa.Column('ip', sa.String(length=255), nullable=True),
    sa.Column('ip_mask1', sa.String(length=255), nullable=True),
    sa.Column('ip_mask2', sa.String(length=255), nullable=True),
    sa.Column('datetime', sa.String(length=255), nullable=True),
    sa.Column('day_hour', sa.String(length=255), nullable=True),
    sa.Column('landing_clicked_datetime', sa.String(length=255), nullable=True),
    sa.Column('destination', sa.String(length=255), nullable=True),
    sa.Column('is_unique_stream', sa.Boolean(), nullable=False),
    sa.Column('is_unique_campaign', sa.Boolean(), nullable=False),
    sa.Column('is_unique_global', sa.Boolean(), nullable=False),
    sa.Column('is_bot', sa.Boolean(), nullable=False),
    sa.Column('is_empty_referrer', sa.Boolean(), nullable=False),
    sa.Column('is_using_proxy', sa.Boolean(), nullable=False),
    sa.Column('landing_clicked', sa.Boolean(), nullable=False),
    sa.Column('is_lead', sa.Boolean(), nullable=False),
    sa.Column('is_sale', sa.Boolean(), nullable=False),
    sa.Column('is_rejected', sa.Boolean(), nullable=False),
    sa.Column('parent_campaign_id', sa.Integer(), nullable=True),
    sa.Column('parent_sub_ids', sa.JSON(), nullable=True),
    sa.Column('cost', sa.Integer(), nullable=True),
    sa.Column('profitability', sa.Integer(), nullable=True),
    sa.Column('revenue', sa.Integer(), nullable=True),
    sa.Column('profit', sa.Integer(), nullable=True),
    sa.Column('lead_revenue', sa.Integer(), nullable=True),
    sa.Column('sale_revenue', sa.Integer(), nullable=True),
    sa.Column('rejected_revenue', sa.Integer(), nullable=True),
    sa.Column('rebills', sa.Integer(), nullable=True),
    sa.Column('landing_clicked_period', sa.Integer(), nullable=True),
    sa.Column('campaign', sa.String(), nullable=True),
    sa.Column('campaign_group', sa.String(), nullable=True),
    sa.Column('offer', sa.String(), nullable=True),
    sa.Column('offer_group', sa.String(), nullable=True),
    sa.Column('stream', sa.String(), nullable=True),
    sa.Column('landing', sa.String(), nullable=True),
    sa.Column('ts', sa.String(), nullable=True),
    sa.Column('affiliate_network', sa.String(), nullable=True),
    sa.Column('lead_id', sa.Integer(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['lead_id'], ['leads.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('lead_messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_scam', sa.Boolean(), nullable=True),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('lead_id', sa.Integer(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['lead_id'], ['leads.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('lead_signals',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('resubscribe', sa.Integer(), nullable=False),
    sa.Column('is_deposit', sa.Boolean(), nullable=False),
    sa.Column('start_subscribe', sa.DateTime(), nullable=True),
    sa.Column('end_subscribe', sa.DateTime(), nullable=True),
    sa.Column('lead_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['lead_id'], ['leads.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('lead_steps',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('started', sa.DateTime(), nullable=True),
    sa.Column('finished', sa.DateTime(), nullable=True),
    sa.Column('lead_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['lead_id'], ['leads.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('message_radist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('radist_contact_chat_id', sa.Integer(), nullable=False),
    sa.Column('inbound_message', sa.Boolean(), nullable=False),
    sa.Column('outbound_message', sa.Boolean(), nullable=False),
    sa.Column('message', sa.Text(), nullable=False),
    sa.Column('radist_influencer_lead_id', sa.Integer(), nullable=False),
    sa.Column('lead_id', sa.Integer(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['lead_id'], ['leads.id'], ),
    sa.ForeignKeyConstraint(['radist_influencer_lead_id'], ['radist_influencer_leads.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('trader_session_announcements',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('remind_interval', sa.Interval(), nullable=False),
    sa.Column('session_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['session_id'], ['trader_sessions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('trader_session_messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('photo_id', sa.String(), nullable=True),
    sa.Column('message_id', sa.Integer(), nullable=False),
    sa.Column('session_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['session_id'], ['trader_sessions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('postback_partners',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('partner_id', sa.Integer(), nullable=False),
    sa.Column('tg_id', sa.BigInteger(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('event_id', sa.String(), nullable=True),
    sa.Column('payout', sa.DECIMAL(), nullable=True),
    sa.Column('link_id', sa.Integer(), nullable=False),
    sa.Column('click_id', sa.String(), nullable=True),
    sa.Column('crm_lead_id', sa.Integer(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['crm_lead_id'], ['crm_leads.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('utm_lead_invites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('number', sa.Integer(), nullable=True),
    sa.Column('invite_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['invite_id'], ['lead_invites.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('lead_partner_rdeps',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('deposit_sum', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('partner_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['partner_id'], ['postback_partners.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('lead_partner_rdeps')
    op.drop_table('utm_lead_invites')
    op.drop_table('postback_partners')
    op.drop_table('trader_session_messages')
    op.drop_table('trader_session_announcements')
    op.drop_table('message_radist')
    op.drop_table('lead_steps')
    op.drop_table('lead_signals')
    op.drop_table('lead_messages')
    op.drop_table('lead_keitaro')
    op.drop_table('lead_invites')
    op.drop_table('lead_influencer_association')
    op.drop_table('lead_channels')
    op.drop_table('lead_bots')
    op.drop_table('crm_leads')
    op.drop_table('crm_contacts')
    op.drop_table('trader_sessions')
    op.drop_table('radist_influencer_leads')
    op.drop_table('leads')
    op.drop_table('channel_posts')
    op.drop_table('trader_session_signals')
    op.drop_table('trader_session_reminders')
    op.drop_table('radist_influencer')
    op.drop_table('crm_users')
    op.drop_table('channels')
    op.drop_table('traders')
    op.drop_table('news')
    op.drop_table('influencers')
    op.drop_table('crms')
    op.drop_table('bot_admins')
    # ### end Alembic commands ###
