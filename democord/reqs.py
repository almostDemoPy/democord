from enum import Enum
from typing import *


class DELETE(Enum):
  """
  Utilizes the DELETE API method
  """

  channel : Callable[[int], str] = lambda channel_id : f"/channels/{channel_id}"
  channel_permission : Callable[[int, int], str] = lambda channel_id, overwrite_id : f"/channels/{channel_id}/permissions/{overwrite_id}"
  guild : Callable[[int], str] = lambda guild_id: f"/guilds/{guild_id}"
  member : Callable[[int, int], str] = lambda guild_id, user_id : f"/guilds/{guild_id}/members/{user_id}"
  member_role : Callable[[int, int, int], str] = lambda guild_id, member_id, role_id : f"/guilds/{guild_id}/members/{member_id}/roles/{role_id}"

class GET(Enum):
  """
  Utilizes the GET API method
  """

  active_threads : str = lambda guild_id: f"/guilds{guild_id}/threads/active"
  channel_invites : Callable[[int], str] = lambda channel_id : f"/channels/{channel_id}/invites"
  gateway        : str = "/gateway"
  guild          : Callable[[int, int], str] = lambda guild_id, with_counts  : f"/guilds/{guild_id}?with_counts={with_counts}"
  guild_channels : Callable[[int], str] = lambda guild_id               : f"/guilds/{guild_id}/channels"
  guild_preview  : Callable[[int], str] = lambda guild_id               : f"/guilds/{guild_id}/preview"
  member         : Callable[[int, int], str] = lambda guild_id, member_id    : f"/guilds/{guild_id}/members/{member_id}"
  members        : Callable[[int, int, int], str] = lambda guild_id, limit, after : f"/guilds/{guild_id}/members?limit={limit}&after={after}"

class PATCH(Enum):
  """
  Utilizes the PATCH API method
  """

  channel : Callable[[int], str] = lambda channel_id : f"/channels/{channel_id}"
  guild : Callable[[int], str] = lambda guild_id: f"/guilds/{guild_id}"
  member : Callable[[int, int], str] = lambda guild_id, member_id : f"/guilds/{guild_id}/members/{member_id}"

class POST(Enum):
  channel_invite : Callable[[int], str] = lambda channel_id : f"/channels/{channel_id}/invites"
  guild : str = "/guilds"

class PUT(Enum):
  channel_permissions : Callable[[int, int], str] = lambda channel_id, overwrites_id : f"/channels/{channel_id}/permissions/{overwrite_id}"
  member : Callable[[int, int], str] = lambda guild_id, user_id : f"/guilds/{guild_id}/members/{user_id}"
  member_role : Callable[[int, int, int], str] = lambda guild_id, member_id, role_id : f"/guilds/{guild_id}/members/{member_id}/roles/{role_id}"