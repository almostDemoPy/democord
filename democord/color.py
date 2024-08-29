from typing import Self

class Color:
  
  @classmethod
  def from_int(cls, value : int) -> Self:
    color : Self = cls()
    color.value : int = value
    return color