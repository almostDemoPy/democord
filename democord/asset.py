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