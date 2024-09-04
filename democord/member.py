from typing import Self
from .user  import User


class Member:
  @classmethod
  def from_data(cls, data : dict) -> Self:
    member : Self = cls()
    for attribute in data:
      match attribute:
        case "user": member.__dict__[attribute] : User = User.from_data(data[attribute])
    return member