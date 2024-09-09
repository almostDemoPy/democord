from .asset   import Asset
from .color   import Color
from .enums   import PremiumType
from .flags   import UserFlags
from .locales import Locale
from typing   import *

if TYPE_CHECKING:
  from .ws    import DiscordWebSocket


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


  @classmethod
  def from_data(
    cls,
    data : Dict[str, Any]
  ) -> Self:
    """
    Construct a User object from a dictionary payload

    Parameters
    ----------
    data : Dict[str, Any]
      Dictionary payload of the User object

    Returns
    -------
    User
    """
    user : Self = cls()
    for attribute in data:
      match attribute:
        case "id" | "discriminator": user.__dict__[attribute] : int = int(data[attribute])
        case "global_name":
          if not data[attribute]: user.__dict__[attribute] : str = data["username"]
          else:                   user.__dict__[attribute] : str = data[attribute]
        case "banner": user.__dict__[attribute] : Asset = Asset.from_user(attribute, data) if data[attribute] else None
        case "avatar":
          user.__dict__[attribute] : str = CallableAvatar(f"https://cdn.discordapp.com/avatars/{data["id"]}/{data["avatar"]}.{"gif" if data["avatar"].startswith("a_") else "png"}") if data[attribute] else ""
          user.default_avatar      : str = f"https://cdn.discordapp.com/embed/avatars/{(int(data["id"]) >> 22) % 6 if int(data["discriminator"]) == 0 else int(data["discriminator"]) % 5}.png"
          user.avatar_decoration   : str = f"https://cdn.discordapp.com/avatar-decoration-presets/{data["avatar_decoration_data"]["asset"]}.png" if data.get("avatar_decoration_data") else ""
        case "accent_color": user.__dict__[attribute] : Color       = Color.from_int(data[attribute])
        case "locale":       user.__dict__[attribute] : Locale      = Locale._value2member_map_[data[attribute]]
        case "flags":        user.__dict__[attribute] : List[str]   = [name for name, flag in UserFlags._member_map_.items() if (data[attribute] & flag.value) == flag.value]
        case "public_flags": user.__dict__[attribute] : List[str]   = [name for name, flag in UserFlags._member_map_.items() if (data[attribute] & flag.value) == flag.value]
        case "premium_type": user.__dict__[attribute] : PremiumType = PremiumType._value2member_map_[data[attribute]]
        case _:              user.__dict__[attribute] : Any         = data[attribute]
    return user


  @classmethod
  def from_id(
    cls,
    ws      : DiscordWebSocket,
    user_id : int
  ) -> Self:
    """
    Construct a User object from a given user ID

    Parameters
    ----------
    user_id : int
      ID of the user to look for
      
    ws : DiscordWebSocket
      Websocket used for the Discord API connection

    Returns
    -------
    User
    """
    if ws.app.members(id = user_id): return ws.app.members(id = user_id)
    user : Self = cls.from_data(ws.get(f"/users/{user_id}"))
    ws.app.members.append(user)
    return user