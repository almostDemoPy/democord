from typing import Self
from .user  import User


class Member:
  @classmethod
  def from_data(cls, data : dict) -> Self:
    member : Self = cls()
    return member