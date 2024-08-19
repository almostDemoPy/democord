from .types import GatewayIntents
from typing import Self


class Intents:
  def __init__(
    self,
    *intents
  ) -> None:
    self._value : int = 0
    for intent in intents:
      assert isinstance(intent, GatewayIntents), "Arguments passed must be a GatewayIntents enum"
      if self._value & intent.value: continue
      self._value |= intent.value


  def __invert__(self, other : Intents) -> Self:
    return ~self._value


  def __and__(self, other : Intents) -> Self:
    self._value |= ~other
    return self._value


  @property
  def value(self) -> int:
    return self._value


  @classmethod
  async def none(cls) -> Self:
    return cls()