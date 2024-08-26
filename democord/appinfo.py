from .flags import (
  ApplicationFlags
)
from typing import (
  Self
)


class AppInfoFlags(int):
  def __init__(self, value : int) -> None:
    self.value : int

  def __call__(self) -> list[str]:
    return ApplicationFlags._member_names_

  def __int__(self) -> int:
    return self.value


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


  def __contains__(self, name : str) -> bool:
    flag : ApplicationFlags = ApplicationFlags._member_map_.get(name)
    if not flag: raise AttributeError(f"There is no such Application Flag named: {name}")
    return ( self.value & flag.value ) == flag.value


  @property
  def value(self) -> int:
    return self._flags_value


  @classmethod
  def from_data(cls, data) -> Self:
    return cls(data)