from .intents  import Intents
from threading import Thread
from .ws       import DiscordWebSocket


class App:
  def __init__(
    self,
    token : str = None
  ) -> None:
    self.__token : str = token
    self.ws : DiscordWebSocket = DiscordWebSocket(self)


  def run(self) -> None:
    self.ws.connect()