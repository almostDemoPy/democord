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


  def add(self, callback) -> None:
    match callback.__name__:
      case "on_ready":
        self.ready.append(callback)


  async def call(self, event : GatewayEvents) -> None:
    tasks = []
    match event:
      case GatewayEvents.Ready:
        for callback in self.ready:
          tasks.append(callback())
    await gather(*tasks)