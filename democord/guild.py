from .asset import Asset
from .channels import (
  GuildChannel
)
from .enums import (
  DefaultMessageNotification,
  ExplicitContentFilter,
  MFALevel,
  NSFWLevel,
  PremiumTier,
  VerificationLevel
)
from .file import File
from .flags import (
  SystemChannelFlags
)
from .reqs import (
  GET,
  PATCH
)
from typing import Self
from .user import User


class CallableSystemChannelFlags(list):
  def __call__(self, flag : SystemChannelFlags) -> bool:
    return flag.name in self


class CallableGuildChannels(list):
  def __call__(self, **kwargs) -> list:
    if not args: return self
    return [
      guild_channel
      for guild_channel in self
      if all(
        guild_channel.__dict__[kwarg] == kwargs[kwarg]
        for kwarg in kwargs
        if guild_channel.__dict__.get(kwarg)
      )
    ]


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


  async def edit(
    self,
    *attributes
  ) -> Self:
    if not attributes: raise MissingArguments("Arguments are required to be filled in this method")
    data : dict = {}
    try:
      for attribute in attributes:
        match attribute:
          case "name":
            if not isinstance(attributes[attribute], str):
              raise TypeError("Guild.name must be of type <str>")
            data[attribute] : str = name
          case "description":
            if not isinstance(attributes[attribute], (str, None)):
              raise TypeError("Guild.description must be of type <str> or <NoneType>")
            data[attribute] : str = attributes[attribute]
          case "verification_level":
            if not isinstance(attributes[attribute], VerificationLevel):
              raise TypeError("Guild.verification_level must be of type <VerificationLevel[Enum]>")
            data[attribute] : int = attributes[attribute].value
          case "default_message_notifications":
            if not isinstance(attributes[attribute], DefaultMessageNotification):
              raise TypeError("Guild.default_message_notifications must be of type <DefaultMessagenotification[Enum]>")
            data[attribute] : int = attributes[attribute].value
          case "explicit_content_filter":
            if not isinstance(attributes[attribute], ExplicitContentFilter):
              raise TypeError("Guild.explicit_content_filter must be of type <ExplicitContentFilter[Enum]>")
            data[attribute] : int = attributes[attribute].value
          case "afk_channel":
            if not isinstance(attributes[attribute], (GuildChannel, int)):
              raise TypeError("Guild.afk_channel_id must either be a <GuildChannel> or <int>")
            data[attribute] : int = int(attributes[attribute])
          case "afk_timeout":
            if not isinstance(attributes[attribute], int): raise TypeError("Guild.afk_timeout must be of type <int>")
            if attributes[attribute] not in [60, 300, 900, 1_800, 3_600]: raise ValueError("Guild.afk_timeout must be of one of the values: 60, 300, 900, 1800, 3600")
            data[attribute] : int = attributes[attribute]
          case "owner_id":
            if not isinstance(attributes[attribute], int): raise TypeError("Guild.owner_id must be of type <int>")
            data[attribute] : int = attributes[attribute]
          case "icon":
            if not isinstance(attributes[attribute], File): raise TypeError("Guild.icon must be of type <File>")
            if attributes[attribute].filename.endswith(".gif") and "ANIMATED_ICON" not in self.features: raise ValueError("Guild is not available for animated icons")
            data[attribute] : int = attributes[attribute].data
    except Exception as error:
      if self.ws.app.logger: self.ws.app.logger.error(error)
    reason : str = str(attributes.get("reason"))
    return self.ws.post(
      PATCH.guild,
      data = data,
      reason = reason
    )


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
        case "verification_level": guild.__dict__[attribute] = VerificationLevel(data[attribute]).name
        case _: guild.__dict__[attribute] = data[attribute]
    guild.channels : CallableGuildChannels(ws, guild)
    return guild