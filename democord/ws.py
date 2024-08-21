import asyncio
import rel
import requests
from json import (
  dumps,
  loads
)
from .payloads import (
  Payload
)
from random import (
  random
)
from threading import (
  Thread
)
from traceback import (
  print_exc
)
from .types import (
  PayloadType,
  GatewayEvents
)
from typing import (
  TYPE_CHECKING
)
from websocket import (
  WebSocketApp
)

if TYPE_CHECKING:
  from .app import App


class DiscordWebSocket:
  def __init__(
    self,
    app : "App"
  ) -> None:
    self.app : App = app
    self.api_version : int = 10
    self.api : str = f"https://discord.com/api/v{self.api_version}"
    self.gateway : str = f"{self.get("/gateway")["url"]}?v={self.api_version}&encoding=json"
    self.connection : WebSocketApp = WebSocketApp(
      self.gateway,
      on_open = self.on_open,
      on_error = self.on_error,
      on_close = self.on_close,
      on_message = self.on_message
    )
    self.heartbeat_interval : int = None
    self.identify_sent : bool = False
    self.last_sequence : int | None = None


  def get(self, endpoint : str) -> dict:
    return loads(requests.get(f"{self.api}{endpoint}").content)


  def post(self, payload : Payload) -> None:
    try:
      print(f"sent     : {payload}")
      self.connection.send(
        dumps(payload.to_json())
      )
    except:
      print_exc()


  def identify(self) -> None:
    payload : Payload = Payload.identify(
      token = self.app._App__token,
      intents = self.app.intents
    )
    self.post(payload)
    self.identify_sent : bool = True


  def connect(self) -> None:
    # Thread(target = self.connection.run_forever).start()
    try:
      self.connection.run_forever(
        dispatcher = rel
      )
      rel.dispatch()
    except KeyboardInterrupt:
      raise KeyboardInterrupt()


  def on_open(self, ws) -> None:
    print("connection opened")


  def on_close(self, ws, status_code, message) -> None:
    print(f"{ws}\n{status_code}\n{loads(message.content)}")


  def on_error(self, ws, error) -> None:
    pass


  def send_heartbeat(self, jitter : bool = False, wait : bool = True) -> None:
    wait_time : int = self.heartbeat_interval
    if jitter: wait_time *= random()
    if wait: asyncio.run(asyncio.sleep(wait_time / 1_000))
    self.post(
      Payload(
        op = PayloadType.HeartBeat,
        d = self.last_sequence
      )
    )


  def on_message(self, ws, message) -> None:
    try:
      print(f"received : {loads(message)}")
      payload : Payload = Payload.from_data(loads(message))
      self.last_sequence : int | None = payload.s
      match payload.op:
        case PayloadType.Hello:
          self.heartbeat_interval : int = payload.d["heartbeat_interval"]
          Thread(target = self.send_heartbeat, kwargs = {"jitter": True}).start()
        case PayloadType.HeartBeatACK:
          if not self.identify_sent:
            Thread(
              target = self.identify
            ).start()
          Thread(target = self.send_heartbeat).start()
        case PayloadType.HeartBeat:
          Thread(target = self.send_heartbeat).start()
        case PayloadType.Dispatch:
          match payload.t:
            case GatewayEvents.Ready:
              print("calling")
              Thread(target = asyncio.run, args = [self.app._App__app_events.call(payload.t)]).start()
    except KeyboardInterrupt:
      raise KeyboardInterrupt("Program was terminated via Ctrl + C")
    except:
      print_exc()