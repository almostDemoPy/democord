from .appinfo  import AppInfo
from .events   import AppEvents
from .intents  import Intents
from threading import Thread
from typing    import Self
from .user     import User
from .ws       import DiscordWebSocket


class CallableGuilds(list):
  def __call__(self, **kwargs) -> list:
    if not kwargs: return self
    return [
      guild
      for guild in self
      if all(
        guild.__dict__[kwarg] == kwargs[kwarg]
        for kwarg in kwargs
        if guild.__dict__.get(kwarg)
      )
    ]


class CallableMembers(list):
  def __call__(self, **kwargs) -> list:
    if not kwargs: return self
    return [
      member
      for member in self
      if all(
        member.__dict__[kwarg] == kwargs[kwarg]
        for kwarg in kwargs
        if kwarg.__dict__.get(kwarg)
      )
    ]


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
    self.guilds : list = CallableGuilds()
    self._guild_join_requests : list = []
    self._appinfo : AppInfo = None
    self.members : list = CallableMembers()


  @property
  def info(self) -> AppInfo:
    return self._appinfo


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
      case "on_ready": self.__app_events.add(func)
      case "on_guild_available": self.__app_events.add(func)


  async def on_ready(self) -> None:
    pass


  async def on_guild_available(self, guild) -> None:
    pass