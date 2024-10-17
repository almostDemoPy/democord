from enum   import Enum
from typing import *


class ApplicationFlags(Enum):
  """
  Enumerates an application's possible flags
  """
  application_command_badge = 1 << 23
  automod                   = 1 << 6
  embedded                  = 1 << 17
  members                   = 1 << 14
  members_limited           = 1 << 15
  message_content           = 1 << 18
  message_content_limited   = 1 << 19
  pending_verification      = 1 << 16
  presence                  = 1 << 12
  presence_limited          = 1 << 13


class ChannelFlags(Enum):
  pinned                      = 1 << 1
  require_tag                 = 1 << 4
  hide_media_download_options = 1 << 15


class SystemChannelFlags(Enum):
  """
  Enumerates a system channel's flags
  """
  suppress_join_notifications                              = 1 << 0
  suppress_premium_subscriptions                           = 1 << 1
  suppress_guild_reminder_notifications                    = 1 << 2
  suppress_join_notification_replies                       = 1 << 3
  suppress_role_subscription_purchase_notifications        = 1 << 4
  suppress_role_subscription_purchase_notification_replies = 1 << 5


class UserFlags(Enum):
  """
  Enumerates a user's possible flags
  """
  staff                = 1 << 0
  partner              = 1 << 1
  hypesquad_events     = 1 << 2
  bug_hunter_level_1   = 1 << 3
  hypesquad_bravery    = 1 << 6
  hypesquad_brilliance = 1 << 7
  hypesquad_balance    = 1 << 8
  early_supporter      = 1 << 9
  team                 = 1 << 10
  bug_hunter_level_2   = 1 << 14
  verified_bot         = 1 << 16
  verified_developer   = 1 << 17
  certified_moderator  = 1 << 18
  http_bot             = 1 << 19
  active_developer     = 1 << 22