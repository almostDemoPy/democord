from .flags import (
  ApplicationFlags
)
from typing import (
  Self
)


class AppInfo:
  def __init__(
    self,
    attributes
  ) -> None:
    for attribute in attributes:
      match attribute:
        case "flags": self.__dict__["flags"] = AppInfoFlags(attributes[attribute])
        case _: self.__dict__[attribute] = attributes[attribute]


  def __getattribute__(self, attribute : str):
    match attribute:
      case "id": return int(self.__dict__["id"])
      case _: return super().__getattribute__(attribute)


  @classmethod
  def from_data(cls, data) -> Self:
    return cls(data)


class AppInfoFlags:
  def __init__(self, bitfield : int) -> None:
    self.value : int = bitfield


  def __contains__(self, name : str) -> bool:
    flag : ApplicationFlags = ApplicationFlags._member_map_.get(name)
    if not flag: raise AttributeError(f"There is no such Application Flag named: {name}")
    return ( self.value & flag.value ) == flag.value