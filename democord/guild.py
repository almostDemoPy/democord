from .asset import Asset
from .enums import (
  DefaultMessageNotification,
  ExplicitContentFilter,
  MFALevel,
  NSFWLevel,
  PremiumTier
)
from .flags import (
  SystemChannelFlags
)
from typing import Self
from .user import User


class CallableSystemChannelFlags(list):
  def __call__(self, flag : SystemChannelFlags) -> bool:
    return flag.name in self


class Guild:
  def __eq__(self, guild) -> bool:
    assert isinstance(guild, (Guild, int)), f"Must be of type Guild or int, not {type(guild)}"
    if isinstance(guild, Guild): return self.id == guild.id
    if isinstance(guild, int): return self.id == guild


  def __int__(self) -> int:
    return self.id


  def __ne__(self, guild) -> bool:
    assert isinstance(guild, (Guild, int)), f"Must be of type Guild or int, not {type(guild)}"
    if isinstance(guild, Guild): return self.id != guild.id
    if isinstance(guild, int): return self.id != guild


  def __str__(self) -> str:
    return self.name


  @classmethod
  def from_data(cls, ws, data : dict) -> Self:
    guild : Self = cls()
    guild.__dict__["ws"] = ws
    for attribute in data:
      match attribute:
        case "icon" | "splash" | "discovery_splash":
          if data[attribute]: guild.__dict__[attribute] = Asset.from_guild(attribute, data)
        case "id": guild.__dict__[attribute] = int(data[attribute])
        case "owner_id": guild.__dict__["owner"] = User.from_id(ws, data["owner_id"])
        case "default_message_notifications": guild.__dict__[attribute] = DefaultMessageNotification(data[attribute]).name
        case "explicit_content_filter": guild.__dict__[attribute] = ExplicitContentFilter(data[attribute]).name
        case "mfa_level": guild.__dict__[attribute] = MFALevel(data[attribute]).name
        case "system_channel_flags": guild.__dict__[attribute] = CallableSystemChannelFlags(name for name, flag in SystemChannelFlags._member_map_.items() if (data[attribute] & flag.value) == flag.value)
        case "premium_tier": guild.__dict__[attribute] = PremiumTier(data[attribute]).name
        case "nsfw_level": guild.__dict__[attribute] = NSFWLevel(data[attribute]).name
        case _: guild.__dict__[attribute] = data[attribute]
    return guild