from typing import Self
from .user  import User


class Member:
  @classmethod
  def from_data(cls, ws, data : dict) -> Self:
    member : Self = cls()
    return member