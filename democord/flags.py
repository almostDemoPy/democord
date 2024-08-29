from enum import Enum


class ApplicationFlags(Enum):
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


class UserFlags(Enum):
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