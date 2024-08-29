from .asset import Asset
from typing import Self
from .user import User


class Guild:
  def __init__(self, ws, data : dict) -> None:
    for attribute in data:
      match attribute:
        case "icon" | "splash" | "discovery_splash":
          if data[attribute]: self.__dict__[attribute] = Asset.from_guild(attribute, data)
        case "id": self.__dict__[attribute] = int(data[attribute])
        case "owner_id": self.__dict__["owner"] = User.from_id(ws, data["owner_id"])
        case _: self.__dict__[attribute] = data[attribute]


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
    return cls(ws, data)