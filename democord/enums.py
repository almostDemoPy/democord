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
  Ready = "READY"
  GuildCreate = "GUILD_CREATE"


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