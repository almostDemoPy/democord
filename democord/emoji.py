from typing import *


class Emoji:
  """
  Represents a Discord emoji
  """

  @classmethod
  def from_data(
    cls,
    data : Dict[str, Any]
  ) -> Self:
    """
    Construct an Emoji object from a payload dictionary


    Parameters
    ----------
    data : Dict[str, Any]
      Emoji payload dictionary


    Returns
    -------
    Emoji
    """
    return cls()