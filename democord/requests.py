from enum import Enum


class GET(Enum):
  gateway = "/gateway"
  guild   = lambda guild_id: f"/guilds/{guild_id}"