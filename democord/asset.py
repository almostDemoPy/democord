from typing import *

if TYPE_CHECKING:
  from .guild import Guild


class Asset:
  """
  Represents a Discord asset

  
  Attributes
  ----------
  key : str
    Hash string of the asset

  url : str
    URL of the asset
  """

  def __hash__(self) -> str:
    """
    Utilizes the built-in hash() function that returns the hash of the asset


    Returns
    -------
    str
    """
    return self.key


  def __str__(self) -> str:
    """
    Utilizes the built-in str() function that returns the URL of the asset


    Returns
    -------
    str
    """
    return self.url

  @classmethod
  def from_user(
    cls,
    asset_type : str,
    user       : Dict[str, Any]
  ) -> Self:
    """
    Constructs an Asset object from a user-level


    Parameters
    ----------
    asset_type : str
      Type of the user-level asset

    user : Dict[str, Any]
      Dictionary payload of the User object
    """
    asset : Self = cls()
    asset.key : str = user[asset_type]
    match asset_type:
      case "avatar": endpoint : str = "avatars"
      case "banner": endpoint : str = "banners"
    asset.url : str = f"https://cdn.discordapp.com/{endpoint}/{user["id"]}/{asset.key}.{"gif" if asset.key.startswith("a_") else "png"}"
    return asset