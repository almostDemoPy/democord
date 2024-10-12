from .enums import ErrorCodes
from .errors import BotMissingPermissions
from .reqs import PATCH
from typing import *


class GuildChannel:
  """
  Represents a guild channel. This can be further classified as TextChannel, VoiceChannel, ForumChannel, StageChannel, and Thread, when subclassed.
  """

  async def move(
    self,
    position : int,
    *,
    lock_permissions : Optional[bool] = False,
    parent : Optional[Union[CategoryChannel, int]] = None
  ) -> Self:
    try:
      if not isinstance(position, int): raise TypeError("GuildChannel.position must be of type <int>")
      if position < 0: raise ValueError("GuildChannel.position must be a positive integer")
      if not isinstance(lock_permissions, bool): raise TypeError("lock_permissions parameter must be of type <bool>")
      if not isinstance(parent, (CategoryChannel, int)): raise TypeError("GuildChannel.parent must be of type <CategoryChannel> or <int>")
      response : Dict[str, Any] = self.ws.patch(
        PATCH.channel_position(self.guild.id),
        data = {
          "id": self.id,
          "position": position,
          "lock_permissions": lock_permissions,
          "parent_id": int(parent) if parent else (int(self.parent) if self.parent else None)
        }
      )
      if response.get("code"):
        match ErrorCodes(response.get("code")):
          case ErrorCodes.BotMissingPermissions:
            raise BotMissingPermissions(PermissionFlags.manage_channels)
      self : Self = GuildChannel.from_data(self.ws, response)
      return self
    except Exception as error:
      if self.ws.app.logger: self.ws.app.logger.error(error)


class TextChannel(GuildChannel): pass