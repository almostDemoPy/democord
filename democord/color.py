from typing import *

class Color:
  """
  Represents a Discord color


  Attributes
  ----------
  hex : str
    Hex value of the color in the form of #000000

  value : int
    The hexadecimal value of the color
  """
  
  @classmethod
  def from_int(
    cls,
    value : int
  ) -> Self:
    """
    Construct a Color object from a hexadecimal value


    Parameters
    ----------
    value : int
      Hexadecimal value of a color


    Returns
    -------
    Color
    """
    color : Self = cls()
    color.value : int = value
    color.hex   : str = hex(value).replace("0x", "#")
    return color

  @classmethod
  def from_rgb(
    cls,
    red   : int = 0,
    green : int = 0,
    blue  : int = 0
  ) -> Self:
    """
    Construct a Color object from an RGB value


    Parameters
    ----------
    red : Optional[int]
      Red value to apply to the color. Defaults to 0
    green : Optional[int]
      Green value to apply to the color. Defaults to 0
    blue : Optional[int]
      Blue value to apply to the color. Defaults to 0


    Returns
    -------
    Color
    """
    color : Self = cls()
    color.value : int = (red * 65536) + (green * 256) + blue
    color.hex   : str = hex(color.value).replace("0x", "#")
    return color