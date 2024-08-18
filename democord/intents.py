from .types import GatewayIntents
from typing import Self


class Intents:
  def __init__(
    self,
    *intents
  ) -> None:
    self.value : int = 0
    for intent in intents:
      assert isinstance(intent, GatewayIntents), "Arguments passed must be a GatewayIntents enum"
      self.value |= intent.value


  @classmethod
  async def none(cls) -> Self:
    return cls()