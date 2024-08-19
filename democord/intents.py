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


  def __and__(self, intent : GatewayIntents) -> Self:
    if self._value & intent.value: return self._value
    self._value |= intent.value
    return self._value


  @property
  def value(self) -> int:
    return self._value


  @classmethod
  async def none(cls) -> Self:
    return cls()