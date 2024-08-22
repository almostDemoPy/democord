from .types import GatewayIntents
from typing import Self


class Intents(object):
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
      assert isinstance(intent, GatewayIntents), f"Arguments passed must be a GatewayIntents enum, not {type(intent)}"
      if ( self._value & intent.value ) == intent.value: continue
      self._value |= intent.value


  def __ior__(self, intent : GatewayIntents) -> Self:
    if not isinstance(intent, GatewayIntents): raise TypeError(f"Type must be GatewayIntents, not {type(intent)}")
    if ( self._value & intent.value ) == self._value: return self
    self._value |= intent.value
    return self


  def __iand__(self, intent : GatewayIntents) -> Self:
    if not isinstance(intent, GatewayIntents): raise TypeError(f"Type must be GatewayIntents, not {type(intent)}")
    self._value &= ~intent.value
    return self


  def __and__(self, intent : GatewayIntents) -> bool:
    if not isinstance(intent, GatewayIntents): raise TypeError(f"Must be GatewayIntents, not {type(intent)}")
    return ( self._value & intent.value ) == intent.value


  def __getitem__(self, intent_name : str | GatewayIntents) -> bool:
    if isinstance(intent_name, GatewayIntents): intent_name : str = intent_name.name
    if intent_name not in GatewayIntents.__dict__["_member_names_"]: raise AttributeError(f"No such intent with name: {intent_name}")
    intent : GatewayIntents = GatewayIntents.__dict__[intent_name]
    return self & intent


  @property
  def value(self) -> int:
    """
    The corresponding bitfield integer of all the passed intents.

    Returns:
      int: The corresponding bitfield integer of all the passed intents.
    """
    return self._value


  @classmethod
  def default(cls) -> Self:
    """
    Creates an Intents instance with all, except the privileged ones, intents enabled.

    Returns: Intents
    """
    return cls(*[intent for intent in GatewayIntents if intent.name not in ["message_content", "presences", "members"]])


  @classmethod
  def none(cls) -> Self:
    """
    Creates an Intents instance with no passed intent.

    Returns: Intents
    """
    return cls()