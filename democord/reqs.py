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
  guild          : str = lambda guild_id, with_counts: f"/guilds/{guild_id}?with_counts={with_counts}"
  guild_channels : str = lambda guild_id             : f"/guilds/{guild_id}/channels"
  guild_preview  : str = lambda guild_id             : f"/guilds/{guild_id}/preview"

class PATCH(Enum):
  """
  Utilizes the PATCH API method
  """

  guild : str = lambda guild_id: f"/guilds/{guild_id}"

class POST(Enum):
  guild : str = "/guilds"