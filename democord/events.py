from .enums    import GatewayEvents
from .guild    import Guild
from asyncio   import (
                      create_task,
                      gather,
                      run as async_run
                      )
from threading import Thread
from traceback import TracebackException
from typing    import *

if TYPE_CHECKING:
  from .app import App


class AppEvents:
  """
  Events handler for the application
  """

  def __init__(
    self,
    app : "App"
  ) -> None:
    self.app                : App             = app
    self.ready              : List[Coroutine] = [self.app.on_ready]
    self.on_guild_available : List[Coroutine] = [self.app.on_guild_available]


  def add(
    self,
    callback : Coroutine
  ) -> None:
    """
    Append the coroutine as an event listener for the application. This is usually called from the @App.listener() decorator


    Parameters
    ----------
    callback : Coroutine
      Function callback coroutine of the event listener
    """
    match callback.__name__:
      case "on_ready":           self.ready.append(callback)
      case "on_guild_available": self.on_guild_available.append(callback)


  async def call(
    self,
    event : GatewayEvents,
    *,
    guild : Optional[Guild] = None
  ) -> None:
    """
    Concurrently call all the event's listener callbacks


    Parameters
    ----------
    event : GatewayEvents
      Type of gateway event triggered

    guild : Optional[Guild]
      Guild object that came with the event
    """
    try:
      tasks = []
      match event:
        case GatewayEvents.Ready:
          for callback in self.ready:
            tasks.append(callback())
            
        case GatewayEvents.GuildCreate:
          for callback in self.on_guild_available:
            if guild not in self.app.guilds: self.app.guilds.append(guild)
            else: tasks.append(callback(guild))
      await gather(*tasks)
    except Exception as error:
      if self.app.logger: self.app.logger.error(error, TracebackException.from_exception(error).stack[1])