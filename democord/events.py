from asyncio import (
  create_task,
  gather,
  run as async_run
)
from threading import Thread
from .enums import (
  GatewayEvents
)
from typing import (
  TYPE_CHECKING
)

if TYPE_CHECKING:
  from .app import App


class AppEvents:
  def __init__(
    self,
    app : "App"
  ) -> None:
    self.app : App = app
    self.ready : list = [self.app.on_ready]
    self.on_guild_available : list = [self.app.on_guild_available]


  def add(self, callback) -> None:
    match callback.__name__:
      case "on_ready": self.ready.append(callback)
      case "on_guild_available": self.on_guild_available.append(callback)


  async def call(self, event : GatewayEvents, *, guild = None) -> None:
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