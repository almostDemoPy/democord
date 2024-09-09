from .appinfo  import AppInfo
from .events   import AppEvents
from .guild    import Guild
from .intents  import Intents
from .logger   import Logger
from .reqs     import GET
from .user     import User
from .ws       import DiscordWebSocket
from threading import Thread
from typing    import *


class CallableGuilds(list):
  def __call__(self, **kwargs) -> Optional[List[Guild] | Guild]:
    """
    Filter the returned list of Guild objects

    Parameters
    ----------
    **kwargs
      Keyword arguments of Guild attributes and values used to filter the results

    Returns
    -------
    Optional[List[Guild] | Guild]
    """
    if not kwargs: return self
    matches : List[Guild] = [
      guild
      for guild in self
      if all(
        guild.__dict__[kwarg] == kwargs[kwarg]
        for kwarg in kwargs
        if guild.__dict__.get(kwarg)
      )
    ]
    return (matches[0] if len(matches) == 1 else matches) if matches else None


class CallableUsers(list):
  def __call__(self, **kwargs) -> Optional[List[User] | User]:
    """
    Filter the returned list of User objects

    Parameters
    ----------
    **kwargs
      User attributes used to filter the returned list of Users

    Returns
    -------
    Optional[List[User] | User]
    """
    if not kwargs: return self
    matches : List[User] = [
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
  """
  Represents a Discord application

  Attributes
  ----------
  guilds  : List[Guild]
    List of guilds the application has access to

  info    : AppInfo
    The application's info data

  intents : int
    Valued intents used for the application

  logger  : Optional[Logger]
    The logger initiated for the application, if enabled

  user    : User
    Corresponding User object of the application

  users   : List[User]
    List of users the application has access to

  ws      : DiscordWebSocket
    WebSocket used for connecting the application to Discord API
  """

  users : list[User] = CallableUsers()

  def __init__(
    self,
    token      : str     = None,
    *,
    intents    : Intents = None,
    logger     : bool    = False,
    debug_mode : bool    = False
  ) -> None:
    """
    Parameters
    ---------
    token : str
      Bot token of the application

    intents : Intents
      The valued intents to use

    logger : Optional[bool]
      Whether to enable the logger for the application. Defaults to False

    debug_mode : Optional[bool]
      Whether to enable debug mode of the logger. This is ignored if logger is False. Defaults to
    """
    self.guilds               : List[Guild]      = CallableGuilds()
    self.logger               : Optional[Logger] = Logger(debug_mode = debug_mode) if logger else None
    self.user                 : User             = None
    self._appinfo             : AppInfo          = None
    self._guild_join_requests : List             = []
    self._intents             : Intents          = intents if intents else Intents.none()
    self._presences           : List             = []
    self._private_channels    : List             = []
    self._relationships       : List             = []
    self._ws                  : DiscordWebSocket = DiscordWebSocket(self)
    self.__app_events         : AppEvents        = AppEvents(self)
    self.__token              : str              = token


  @property
  def info(self) -> AppInfo:
    """
    The application's info data

    Returns
    -------
    AppInfo
    """
    return self._appinfo


  @property
  def intents(self) -> int:
    """
    Valued intents used for the application

    Returns
    -------
    int
    """
    return self._intents.value


  @property
  def ws(self) -> DiscordWebSocket:
    """
    WebSocket used for connecting to Discord API

    Returns
    -------
    DiscordWebSocket
    """
    return self._ws


  def run(self) -> None:
    """
    Login and connect to the gateway
    """
    self.ws.connect()


  def event(
    self,
    function : Coroutine
  ) -> None:
    """
    Register a function as an event listener for the application. This is typically used as a decorator

    Parameters
    ----------
    function : Coroutine
      The function to append as an event listener
    """
    match function.__name__:
      case "on_ready"          : self.__app_events.add(function)
      case "on_guild_available": self.__app_events.add(function)


  async def fetch_guild(
    self,
    guild_id    : int,
    /,
    *,
    with_counts : bool = False
  ) -> Optional[Guild]:
    """
    Fetch a guild based from the given guild ID. Returns None if no guild with the specified ID was found.

    Parameters
    ----------
    guild_id : int
      Guild ID of the guild to look for


    Returns
    -------
    Optional[Guild]
    """
    assert isinstance(with_counts, bool), "with_counts argument must be a boolean"
    return Guild.from_data(
      self.ws,
      self.ws.get(
        GET.guild(
          guild_id,
          with_counts
        )
      )
    )


  async def on_ready(self) -> None:
    """
    Called from the READY gateway event
    """
    pass


  async def on_guild_available(
    self,
    guild : Guild
  ) -> None:
    """
    Called from the GUILD_CREATE gateway event

    Parameters
    ----------
    guild : Guild
      The guild object that became available
    """
    pass