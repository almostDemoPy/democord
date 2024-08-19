from .intents  import Intents
from threading import Thread
from .ws       import DiscordWebSocket


class App:
  def __init__(
    self,
    token : str = None,
    *,
    intents : Intents | None = None
  ) -> None:
    self.__token : str = token
    self._ws : DiscordWebSocket = DiscordWebSocket(self)
    self._intents : Intents = intents if intents else Intents.none()


  @property
  def intents(self) -> None:
    return self._intents.value


  @property
  def ws(self) -> DiscordWebSocket:
    return self._ws


  def run(self) -> None:
    self.ws.connect()