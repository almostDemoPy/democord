from typing import Self
from .user  import User


class Member:
  @property
  def id(self) -> int:
    return self.user.id

  @classmethod
  def from_data(cls, data : dict) -> Self:
    member : Self = cls()
    for attribute in data:
      match attribute:
        case "user": member.__dict__[attribute] : User = User.from_data(data[attribute])
        case "nick": member.__dict__[attribute] : str  = data[attribute]
    return member