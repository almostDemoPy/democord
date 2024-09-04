from typing import Self


class Emoji:
  @classmethod
  def from_data(cls, data : dict) -> Self:
    return cls()