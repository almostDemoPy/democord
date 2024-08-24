from enum import Enum


class ApplicationFlags(Enum):
  application_command_badge = 1 << 23
  automod                   = 1 << 6
  embedded                  = 1 << 17
  members                   = 1 << 14 | 1 << 15
  message_content           = 1 << 18 | 1 << 19
  pending_verification      = 1 << 16
  presence                  = 1 << 12 | 1 << 13