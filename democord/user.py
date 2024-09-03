from .asset   import Asset
from .color   import Color
from .enums   import PremiumType
from .flags   import UserFlags
from .locales import Locale
from typing   import Self


class CallableAvatar(str):
  def default(self) -> str | None:
    return self.default_avatar

  def decoration(self) -> str | None:
    return self.avatar_decoration

  def __str__(self) -> str:
    if not self: return self.default()
    return self


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
        case "banner": user.__dict__[attribute] : Asset = Asset.from_user(attribute, data) if data[attribute] else None
        case "avatar":
          user.__dict__[attribute] : str = CallableAvatar(f"https://cdn.discordapp.com/avatars/{data["id"]}/{data["avatar"]}.{"gif" if data["avatar"].startswith("a_") else "png"}") if data[attribute] else ""
          user.default_avatar : str = f"https://cdn.discordapp.com/embed/avatars/{(int(data["id"]) >> 22) % 6 if int(data["discriminator"]) == 0 else int(data["discriminator"]) % 5}.png"
          user.avatar_decoration : str = f"https://cdn.discordapp.com/avatar-decoration-presets/{data["avatar_decoration_data"]["asset"]}.png" if data.get("avatar_decoration_data") else ""
        case "accent_color": user.__dict__[attribute] : Color = Color.from_int(data[attribute])
        case "locale": user.__dict__[attribute] : Locale = Locale._value2member_map_[data[attribute]]
        case "flags": user.__dict__[attribute] : list = [name for name, flag in UserFlags._member_map_.items() if (data[attribute] & flag.value) == flag.value]
        case "public_flags": user.__dict__[attribute] : list = [name for name, flag in UserFlags._member_map_.items() if (data[attribute] & flag.value) == flag.value]
        case "premium_type": user.__dict__[attribute] = PremiumType._value2member_map_[data[attribute]]
        case _: user.__dict__[attribute] = data[attribute]
    return user


  @classmethod
  def from_id(cls, ws, user_id : int) -> Self:
    if ws.app.members(id = user_id): return ws.app.members(id = user_id)[0]
    user : Self = cls.from_data(ws.get(f"/users/{user_id}"))
    ws.app.members.append(user)
    return user