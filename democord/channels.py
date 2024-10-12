from typing import *


class GuildChannel:
  """
  Represents a guild channel. This can be further classified as TextChannel, VoiceChannel, ForumChannel, StageChannel, and Thread, when subclassed.
  """

  pass


class TextChannel(GuildChannel): pass