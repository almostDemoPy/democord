from asyncio import (
  create_task,
  gather,
  run as async_run
)
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


  async def call(self, event : GatewayEvents) -> None:
    tasks = []
    match event:
      case GatewayEvents.Ready:
        print("called")
        for callback in self.ready:
          await create_task(callback())
        print("done")