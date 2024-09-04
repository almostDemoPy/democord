from typing import Self
from .user  import User


class Member:
  @classmethod
  def from_data(cls, ws, data : dict) -> Self:
    member : Self = cls()
    for attribute in data:
      match attribute:
        case "user": member.__dict__[attribute] = User.from_data(data)
    return member