from enum import (
  Enum
)


class PayloadType(Enum):
  Dispatch            = 0
  HeartBeat           = 1
  Identify            = 2
  PresenceUpdate      = 3
  VoiceStateUpdate    = 4
  Resume              = 6
  Reconnect           = 7
  RequestGuildMembers = 8
  InvalidSession      = 9
  Hello               = 10
  HeartBeatACK        = 11


class GatewayEvents(Enum):
  GuildCreate = "GUILD_CREATE"
  Ready       = "READY"
  Resumed     = "RESUMED"


class GatewayIntents(Enum):
  guilds                = 1 << 0
  members               = 1 << 1
  moderation            = 1 << 2
  emojis_and_stikers    = 1 << 3
  integrations          = 1 << 4
  webhooks              = 1 << 5
  invites               = 1 << 6
  voice_states          = 1 << 7
  presences             = 1 << 8
  messages              = ( 1 << 9  ) | ( 1 << 12 )
  reactions             = ( 1 << 10 ) | ( 1 << 13 )
  typing                = ( 1 << 11 ) | ( 1 << 14 )
  message_content       = 1 << 15
  scheduled_events      = 1 << 16
  automod_configuration = 1 << 20
  automod_execution     = 1 << 21
  polls                 = ( 1 << 24 ) | ( 1 << 25 )


class PremiumType(Enum):
  none          = 0
  nitro_classic = 1
  nitro         = 2
  nitro_basic   = 3


class DefaultMessageNotification(Enum):
  all_messages  = 0
  only_mentions = 1


class ExplicitContentFilter(Enum):
  disabled              = 0
  members_without_roles = 1
  all_members           = 2


class MFALevel(Enum):
  none     = 0
  elevated = 1


class PremiumTier(Enum):
  none   = 0
  tier_1 = 1
  tier_2 = 2
  tier_3 = 3


class NSFWLevel(Enum):
  default        = 0
  explicit       = 1
  safe           = 2
  age_restricted = 3