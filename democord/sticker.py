from typing import *


class Sticker:

  @classmethod
  def from_data(cls, data : Dict[str, Any]) -> Self:
    sticker : Self = cls()
    return sticker