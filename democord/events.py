from asyncio import (
  create_task,
  gather,
  run as async_run
)
from threading import Thread
from .types import (
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
    print("adding event")
    match callback.__name__:
      case "on_ready":
        self.ready.append(callback)
        print("event added")


  async def call(self, event : GatewayEvents) -> None:
    tasks = []
    match event:
      case GatewayEvents.Ready:
        print("called")
        for callback in self.ready:
          tasks.append(callback())
    await gather(*tasks)
    print("done")