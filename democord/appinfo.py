from typing import (
  Self
)


class AppInfo:
  def __init__(
    self,
    attributes
  ) -> None:
    for attribute in attributes:
      self.__dict__[attribute] = attributes[attribute]


  def __getattribute__(self, attribute : str):
    match attribute:
      case "id": return int(self.__dict__["id"])
      case _: return super().__getattribute__(attribute)


  @classmethod
  def from_data(cls, data) -> Self:
    return cls(data)