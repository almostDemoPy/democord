from .appinfo  import AppInfo
from .channels import GuildChannel
from .enums    import (
                      DefaultMessageNotification,
                      ExplicitContentFilter,
                      VerificationLevel
                      )
from .errors   import APILimit
from .events   import AppEvents
from .flags    import SystemChannelFlags
from .guild    import Guild
from .intents  import Intents
from .logger   import Logger
from .reqs     import GET, POST
from .role     import Role
from .user     import User
from .ws       import DiscordWebSocket
from dotenv    import load_dotenv
from os        import getenv
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
        if user.__dict__.get(kwarg)
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
    *,
    intents    : Intents = None,
    logger     : bool    = False,
    debug_mode : bool    = False
  ) -> None:
    """
    Parameters
    ---------
    intents : Intents
      The valued intents to use

    logger : Optional[bool]
      Whether to enable the logger for the application. Defaults to False

    debug_mode : Optional[bool]
      Whether to enable debug mode of the logger. This is ignored if logger is False. Defaults to
    """
    load_dotenv()
    self.__app_events         : AppEvents        = AppEvents(self)
    self.__token              : str              = getenv("TOKEN")
    if not self.__token:
      raise Exception("No TOKEN environment variable was found.")
    self._appinfo             : AppInfo          = None
    self._guild_join_requests : List             = []
    self._presences           : List             = []
    self._private_channels    : List             = []
    self._relationships       : List             = []
    self._ws                  : DiscordWebSocket = DiscordWebSocket(self)
    self.guilds               : List[Guild]      = CallableGuilds()
    self.intents              : Intents          = intents if intents else Intents.none()
    self.logger               : Optional[Logger] = Logger(debug_mode = debug_mode) if logger else None
    self.user                 : User             = None


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


  def listen(self, event_name = None) -> Callable:
    def wrapper(function : Callable) -> None:
      self.__app_events.add(event_name or function.__name__, function)
    return wrapper


  async def create_guild(
    self,
    name : str,
    **attributes
  ) -> Guild:
    try:
      if len(self.guilds) >= 10:
        raise APILimit("Bot can only create guilds when in less than 10 guilds.")
      if len(name) < 2 or len(name) > 100:
        raise ValueError("Guild.name length must be between 2 and 100")
      data : Dict[str, Any] = {
        "name": name
      }
      for attribute in attributes:
        match attribute:
          case "afk_channel":
            if not isinstance(attributes[attribute], GuildChannel):
              raise TypeError("Guild.afk_channel must be of type <GuildChannel>")
            data[attribute] : int = int(GuildChannel)
          case "afk_timeout":
            if not isinstance(attributes[attribute], int):
              raise TypeError("Guild.afk_timeout must be of type <int>")
            if attributes[attribute] not in [60, 300, 900, 1_800, 3_600]:
              raise ValueError("Guild.afk_timeout must be of either values: 60, 300, 900, 1800, 3600")
            data[attribute] : int = attributes[attribute]
          case "channels":
            if not isinstance(attributes[attribute], list) and not all(isinstance(channel, GuildChannel) for channel in attributes[attribute]):
              raise TypeError("Guild.channels must be a list of type <GuildChannel>")
            data[attribute] : List[Dict[str, Any]] = [
              channel.data
              for channel in attributes[attribute]
            ]
          case "default_message_notifications":
            if not isinstance(attributes[attribute], DefaultMessageNotifications):
              raise TypeError("Guild.default_message_notifications must be of type <DefaultMessageNotifications>")
            data[attribute] : int = attributes[attribute].value
          case "explicit_content_filter":
            if not isinstance(attributes[attribute], ExplicitContentFilter):
              raise TypeError("Guild.explicit_content_filter must be of type <ExplicitContentFilter>")
            data[attribute] : int = attributes[attribute].value
          case "icon":
            if not isinstance(attributes[attribute], File):
              raise TypeError("Guild.icon must be of type <File>")
            data[attribute] : str = attributes[attribute].data
          case "roles":
            if not isinstance(attributes[attribute], list) and not all(isinstance(role, Role) for role in attributes[attribute]):
              raise TypeError("Guild.roles must be a list of type <Role>")
            data[attribute] : List[Dict[str, Any]] = [
              role.data
              for role in attributes[attribute]
            ]
          case "system_channel":
            if not isinstance(attributes[attribute], GuildChannel):
              raise TypeError("Guild.system_channel must be of type <GuildChannel>")
            data[attribute] : int = int(attributes[attribute])
          case "system_channel_flags":
            if not isinstance(attributes[attribute], list) and not all(isinstance(flag, SystemChannelFlags) for flag in attributes[attribute]):
              raise TypeError("Guild.system_channel_flags must be a list of type <SystemChannelFlags>")
            for flag in attributes[attribute]:
              data[attribute] |= flag.value
          case "verification_level":
            if not isinstance(attributes[attribute], VerificationLevel):
              raise TypeError("Guild.verification_level must be of type <VerificationLevel>")
            data[attribute] : int = attributes[attribute].value
      response : Dict[str, Any] = self.ws.post(
        POST.guilds,
        data = data
      )
      return Guild.from_data(self.ws, response)
    except Exception as error:
      if self.logger: self.logger.error(error)


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