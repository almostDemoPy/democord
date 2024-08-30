from .asset   import Asset
from .color   import Color
from .enums   import PremiumType
from .flags   import UserFlags
from .locales import Locale
from typing   import Self


class User:
  def __getattr__(self, attribute : str) -> None:
    raise AttributeError(f"User object has no attribute: {attribute}")


  @classmethod
  def from_data(cls, data : dict) -> Self:
    user : Self = cls()
    for attribute in data:
      match attribute:
        case "id" | "discriminator": user.__dict__[attribute] = int(data[attribute])
        case "global_name":
          if not data[attribute]: user.__dict__[attribute] = data["username"]
          else: user.__dict__[attribute] = data[attribute]
        case "avatar" | "banner": user.__dict__[attribute] : Asset = Asset.from_user(attribute, data) if data[attribute] else None
        case "accent_color": user.__dict__[attribute] : Color = Color.from_int(data[attribute])
        case "locale": user.__dict__[attribute] : Locale = Locale._value2member_map_[data[attribute]]
        case "flags": user.__dict__[attribute] : list = [name for name, value in UserFlags._member_map_.items() if (data[attribute] & value) == value]
        case "public_flags": user.__dict__[attribute] : list = [name for name, value in UserFlags._member_map_.items() if (data[attribute] & value) == value]
        case "premium_type": user.__dict__[attribute] = PremiumType._value2member_map_[data[attribute]]
        case _: user.__dict__[attribute] = data[attribute]
    return user


  @classmethod
  def from_id(cls, ws, user_id : int) -> Self:
    if ws.app.members(id = user_id): return ws.app.members(id = user_id)[0]
    user : Self = cls.from_data(ws.get(f"/users/{user_id}"))
    ws.app.members.append(user)
    return user