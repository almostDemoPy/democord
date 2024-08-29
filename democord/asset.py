from typing import (
  Self,
  TYPE_CHECKING
)


if TYPE_CHECKING:
  from .guild import Guild


class Asset:
  def __hash__(self) -> str:
    return self.key


  def __str__(self) -> str:
    return self.url


  @classmethod
  def from_guild(cls, asset_type : str, guild : dict) -> Self:
    asset : Self = cls()
    asset.key : str = guild[asset_type]
    match asset_type:
      case "discovery_splash": endpoint : str = "discovery_splashes"
      case "icon": endpoint : str = "icons"
      case "splash": endpoint : str = "splashes"
    asset.url : str = f"https://cdn.discordapp.com/{endpoint}/{guild["id"]}/{asset.key}.{"gif" if asset.key.startswith("a_") else "png"}"
    return asset

  @classmethod
  def from_user(cls, asset_type : str, user : dict) -> Self:
    print(f"asset : {user[asset_type]}")
    asset : Self = cls()
    asset.key : str = user[asset_type]
    match asset_type:
      case "avatar": endpoint : str = "avatars"
    asset.url : str = f"https://cdn.discordapp.com/{endpoint}/{user["id"]}/{asset.key}.{"gif" if asset.key.startswith("a_") else "png"}"
    return asset