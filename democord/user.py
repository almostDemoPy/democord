from .asset       import Asset
from .color       import Color
from .constructor import Constructor
from .enums       import PremiumType
from .flags       import UserFlags
from .locales     import Locale
from typing       import *

if TYPE_CHECKING:
  from .ws        import DiscordWebSocket


class CallableAvatar(str):
  """
  Callable property for User.avatar attribute
  """

  def default(
    self
  ) -> str:
    """
    Returns the default avatar URL of the user
    
    Returns
    -------
    str
    """
    return self.default_avatar

  def decoration(
    self
  ) -> Optional[str]:
    """
    Returns the avatar decoration asset URL of the user, if any

    Returns
    -------
    Optional[str]
    """
    return self.avatar_decoration

  def __str__(
    self
  ) -> str:
    """
    Returns the set avatar of the user. If none is applied, returns the default avatar instead

    Returns
    -------
    str
    """
    if not self: return self.default()
    return self


class User:
  """
  Represents a Discord user
  """

  def __getattr__(self, attribute : str) -> None:
    raise AttributeError(f"User object has no attribute: {attribute}")