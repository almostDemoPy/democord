from enum import Enum
from typing import *


class DELETE(Enum):
  """
  Utilizes the DELETE API method
  """

  guild : str = lambda guild_id: f"/guilds/{guild_id}"

class GET(Enum):
  """
  Utilizes the GET API method
  """

  gateway        : str = "/gateway"
  guild          : str = lambda guild_id, with_counts  : f"/guilds/{guild_id}?with_counts={with_counts}"
  guild_channels : str = lambda guild_id               : f"/guilds/{guild_id}/channels"
  guild_preview  : str = lambda guild_id               : f"/guilds/{guild_id}/preview"
  member         : str = lambda guild_id, member_id    : f"/guilds/{guild_id}/members/{member_id}"
  members        : str = lambda guild_id, limit, after : f"/guilds/{guild_id}/members?limit={limit}&after={after}"

class PATCH(Enum):
  """
  Utilizes the PATCH API method
  """

  guild : str = lambda guild_id: f"/guilds/{guild_id}"
  member : str = lambda guild_id, member_id : f"/guilds/{guild_id}/members/{member_id}"

class POST(Enum):
  guild : str = "/guilds"

class PUT(Enum):
  member : str = lambda guild_id, user_id : f"/guilds{guild_id}/members/{user_id}"