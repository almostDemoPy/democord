from .appinfo  import AppInfo
from .events   import AppEvents
from .guild    import Guild
from .intents  import Intents
from .logger   import Logger
from .reqs     import GET
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


class CallableUsers(list):
  def __call__(self, **kwargs) -> list[User] | User | None:
    if not kwargs: return self
    matches : list[User] = [
      user
      for user in self
      if all(
        user.__dict__[kwarg] == kwargs[kwarg]
        for kwarg in kwargs
        if kwargs.__dict__.get(kwarg)
      )
    ]
    return (matches[0] if len(matches) == 1 else matches) if matches else None


class App:
  users : list[User] = CallableUsers()

  def __init__(
    self,
    token : str = None,
    *,
    intents : Intents | None = None,
    logger : bool = False,
    debug_mode : bool = False
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
    self.logger : Logger | None = Logger(debug_mode = debug_mode) if logger else None


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


  async def fetch_guild(self, guild_id : int, /, *, with_counts : bool = False) -> Guild | None:
    assert isinstance(with_counts, bool), "with_counts argument must be a boolean"
    return Guild.from_data(self.ws, self.ws.get(GET.guild(guild_id, with_counts)))


  async def on_ready(self) -> None:
    pass


  async def on_guild_available(self, guild : Guild) -> None:
    pass