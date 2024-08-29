from .asset import Asset
from typing import Self


class User:
  def __init__(
    self,
    data : dict[str, str | bool | int | dict | None]
  ) -> None:
    for attribute in data:
      match attribute:
        case "id" | "discriminator": self.__dict__[attribute] = int(data[attribute])
        case "global_name":
          if not data[attribute]: self.__dict__[attribute] = data["username"]
          else: self.__dict__[attribute] = data[attribute]
        case "avatar": self.__dict__[attribute] = Asset.from_user(attribute, data) if data[attribute] else None
        case _: self.__dict__[attribute] = data[attribute]


  def __getattr__(self, attribute : str) -> None:
    raise AttributeError(f"User object has no attribute: {attribute}")


  @classmethod
  def from_data(cls, data : dict) -> Self:
    return cls(data)


  @classmethod
  def from_id(cls, ws, user_id : int) -> Self:
    if ws.app.members(id = user_id): return ws.app.members(id = user_id)[0]
    user : Self = cls.from_data(ws.get(f"/users/{user_id}"))
    ws.app.members.append(user)
    return user