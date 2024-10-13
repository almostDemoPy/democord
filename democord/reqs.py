from enum import Enum
from typing import *


class DELETE(Enum):
  """
  Utilizes the DELETE API method
  """

  guild : Callable[[int], str] = lambda guild_id: f"/guilds/{guild_id}"
  member : Callable[[int, int], str] = lambda guild_id, user_id : f"/guilds/{guild_id}/members/{user_id}"
  member_role : Callable[[int, int, int], str] = lambda guild_id, member_id, role_id : f"/guilds/{guild_id}/members/{member_id}/roles/{role_id}"

class GET(Enum):
  """
  Utilizes the GET API method
  """

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

  guild : Callable[[int], str] = lambda guild_id: f"/guilds/{guild_id}"
  member : Callable[[int, int], str] = lambda guild_id, member_id : f"/guilds/{guild_id}/members/{member_id}"

class POST(Enum):
  guild : str = "/guilds"

class PUT(Enum):
  member : Callable[[int, int], str] = lambda guild_id, user_id : f"/guilds{guild_id}/members/{user_id}"
  member_role : Callable[[int, int, int], str] = lambda guild_id, member_id, role_id : f"/guilds/{guild_id}/members/{member_id}/roles/{role_id}"