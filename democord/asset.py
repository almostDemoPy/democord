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
  def from_guild(cls, guild : Guild) -> Self:
    asset : Self = cls()
    asset.key : str = guild.icon
    asset.url : str = f"https://cdn.discordapp.com/icons/{guild.id}/{asset.key}.{"gif" if asset.key.startswith("a_") else "png"}"
    return asset