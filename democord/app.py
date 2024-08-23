from .events   import AppEvents
from .intents  import Intents
from threading import Thread
from typing    import Self
from .user     import User
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
    self.__app_events : AppEvents = AppEvents(self)
    self.user : User = None
    self._relationships : list = []
    self._private_channels : list = []
    self._presences : list = []
    self._guilds : list = []
    self._guild_join_requests : list = []
    self._id : int = None
    self._flags : int = 0


  @property
  def application_id(self) -> int:
    return self._id


  @property
  def intents(self) -> int:
    return self._intents.value


  @property
  def ws(self) -> DiscordWebSocket:
    return self._ws


  def run(self) -> None:
    self.ws.connect()


  def event(self, func) -> None:
    match func.__name__:
      case "on_ready":
        self.__app_events.add(func)


  async def on_ready(self) -> None:
    pass