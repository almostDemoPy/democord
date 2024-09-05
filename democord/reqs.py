from enum import Enum


class GET(Enum):
  gateway = "/gateway"
  guild   = lambda guild_id, with_counts: f"/guilds/{guild_id}?with_counts={with_counts}"


class PATCH(Enum):
  guild = lambda guild_id: f"/guilds/{guild_id}"