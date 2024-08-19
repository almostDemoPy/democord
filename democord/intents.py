from .types import GatewayIntents
from typing import Self


class Intents:
  """
  Holds the intents the app is going to use.

  Attributes:
    value (int): The corresponding bitfield integer of all the passed intents.
  """


  def __init__(
    self,
    *intents
  ) -> None:
    """
    Initialize an Intents instance

    Parameters:
      intents (Union[GatewayIntents]): Gateway intents to pass for the bot.
    """
    self._value : int = 0
    for intent in intents:
      assert isinstance(intent, GatewayIntents), "Arguments passed must be a GatewayIntents enum"
      if self._value & intent.value: continue
      self._value |= intent.value


  def __ior__(self, intent : GatewayIntents) -> Self:
    if self._value & intent.value: return self
    self._value |= intent.value
    return self


  def __iand__(self, intent : GatewayIntents) -> Self:
    self._value &= ~intent.value
    return self


  def __and__(self, intent : GatewayIntents) -> bool:
    return self._value & intent.value


  @property
  def value(self) -> int:
    """
    The corresponding bitfield integer of all the passed intents.

    Returns:
      int: The corresponding bitfield integer of all the passed intents.
    """
    return self._value


  @classmethod
  async def none(cls) -> Self:
    """
    Creates an Intents instance with no passed intent.

    Returns:
      Intents: An Intents instance with no passed intent.
    """
    return cls()