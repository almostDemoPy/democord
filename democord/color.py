from typing import Self

class Color:
  
  @classmethod
  def from_int(cls, value : int) -> Self:
    color : Self = cls()
    color.value : int = value
    color.hex : str = hex(value).replace("0x", "#")
    return color

  @classmethod
  def from_rgb(cls, red : int = 0, green : int = 0, blue : int = 0) -> Self:
    color : Self = cls()
    color.value : int = (red * 65536) + (green * 256) + blue
    color.hex : str = hex(color.value).replace("0x", "#")
    return color