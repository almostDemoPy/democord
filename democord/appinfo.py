from .flags import (
  ApplicationFlags
)
from typing import (
  Self
)


class CallableInstance:
  def __init__(self, instance):
    self.instance = instance

  def __repr__(self) -> str:
    return str(self.instance._flags_value)


  def __call__(self):
    return self.instance


class AppInfoFlags:
  def __get__(self, instance, owner):
    return CallableInstance(instance)


class AppInfo:

  flags = AppInfoFlags()

  def __init__(
    self,
    attributes
  ) -> None:
    for attribute in attributes:
      match attribute:
        case "flags": self.__dict__["_flags_value"] = attributes[attribute]
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