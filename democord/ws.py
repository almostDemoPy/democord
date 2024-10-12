import asyncio
import rel
import requests
 
from .appinfo  import AppInfo
from .enums    import (
                      GatewayEvents,
                      PayloadType
                      )
from .guild    import Guild
from .payloads import Payload
from .reqs     import (
                      GET,
                      PATCH
                      )
from .user     import User
from json      import (
                      dumps,
                      loads
                      )
from random    import random
from threading import Thread
from traceback import print_exc
from typing    import *
from websocket import WebSocketApp

if TYPE_CHECKING:
  from .app import App


class DiscordWebSocket:
  """
  Websocket handler for the connection to the Discord API and Gateway


  Attributes
  ----------
  app : App
    The application the connection holds

  connection : WebSocketApp
    Websocket connection to the API and gateway

  heartbeat_interval : int
    Interval ( in milliseconds ) used for the delay of sending heartbeats

  last_sequence : Optional[int]
    Last received sequence number

  __resume_gateway_url : str
    The Gateway URL used for resuming connections, if possible

  __session_id : int
    Session ID of the connection
  """

  def __init__(
    self,
    app : "App"
  ) -> None:
    self.app                  : "App"           = app
    self.api_version          : int           = 10
    self.api                  : str           = f"https://discord.com/api/v{self.api_version}"
    self.gateway              : str           = f"{self.get("/gateway")["url"]}?v={self.api_version}&encoding=json"
    self.connection           : WebSocketApp  = WebSocketApp(
      self.gateway,
      on_open    = self.on_open,
      on_error   = self.on_error,
      on_close   = self.on_close,
      on_message = self.on_message
    )
    self.heartbeat_interval   : int           = None
    self.identify_sent        : bool          = False
    self.is_resuming          : bool          = False
    self.last_sequence        : Optional[int] = None
    self.__resume_gateway_url : str           = None
    self.__session_id         : str           = None


  def delete(
    self,
    endpoint : str
  ) -> Dict[str, Any]:
    return loads(
      requests.delete(
        f"{self.api}{endpoint}",
        headers = {
          "Authorization": f"Bot {self.app._App__token}"
        }
      ).content
    )


  def get(
    self,
    endpoint : str
  ) -> Dict[str, Any]:
    """
    Utilizes the GET API method and with an endpoint call

    Parameters
    ----------
    endpoint : str
      The endpoint to call

    Returns
    -------
    Dict[str, Any]
    """
    return loads(
      requests.get(
        f"{self.api}{endpoint}",
        headers = {
          "Authorization": f"Bot {self.app._App__token}"
        }
      ).content
    )

  def patch(
    self,
    endpoint : str,
    data     : Dict[str, Any],
    reason   : Optional[str] = None
  ) -> Dict[str, Any]:
    """
    Utilizes the PATCH API method with an endpoint call

    Parameters
    ----------
    endpoint : str
      The endpoint to call

    data : Dict[str, Any]
      Data to submit to the call

    reason : Optional[str]
      Reason of modification / call

    Returns
    -------
    Dict[str, Any]
    """

    return loads(
      requests.patch(
        f"{self.api}{endpoint}",
        headers = {
          "Authorization"     : f"Bot {self.app._App__token}",
          "Content-Type"      : "application/json",
          "X-Audit-Log-Reason": reason
        },
        data    = dumps(data)
      ).content
    )

  def post(
    self,
    endpoint : str,
    data     : Dict[str, Any],
    reason   : Optional[str] = None
  ) -> Dict[str, Any]:
    return loads(
      requests.post(
        f"{self.api}{endpoint}",
        headers = {
          "Authorization"      : f"Bot {self.app._App__token}",
          "Content-Type"       : "application/json",
          "X-Audit-Log-Reason" : reason
        },
        data    = dumps(data)
      ).content
    )


  def send(
    self,
    payload : Payload
  ) -> None:
    """
    Sends a payload to the connection

    Parameters
    ----------
    payload : Payload
      Payload object to send
    """
    try:
      if self.app.logger and self.app.logger.debug_mode: self.app.logger.debug(f"sent     : {payload}")
      self.connection.send(
        dumps(
          payload.to_json()
        )
      )
    except Exception as error:
      if self.app.logger: self.app.logger.error(error)


  def identify(
    self
  ) -> None:
    """
    Sends an Identify payload
    """
    payload : Payload = Payload.identify(
      token   = self.app._App__token,
      intents = self.app.intents.value
    )
    self.send(
      payload
    )
    self.identify_sent : bool = True
    if self.app.logger and self.app.logger.debug_mode: self.app.logger.debug("Identify payload sent successfully")


  def connect(
    self
  ) -> None:
    """
    Connects to the gateway
    """
    # Thread(target = self.connection.run_forever).start()
    try:
      self.connection.run_forever(
        dispatcher = rel,
        reconnect  = 0
      )
      rel.signal(
        2,
        rel.abort
      )
      rel.dispatch()
      if self.is_resuming:
        Thread(
          target = self.send_heartbeat
        ).start()
        self.send(
          Payload(
            op = PayloadType.Resume,
            d  = {
              "token"      : self.app._App__token,
              "session_id" : self.__session_id,
              "seq"        : self.last_sequence
            }
          )
        )
        self.is_resuming : bool = False
    except Exception as error:
      if self.app.logger: self.app.logger.error(error)

  def resume(
    self
  ) -> None:
    """
    Resumes the connection, if possible
    """

    self.connection.close()
    self.connection : WebSocketApp = WebSocketApp(
      self.__resume_gateway_url,
      on_open    = self.on_open,
      on_error   = self.on_error,
      on_close   = self.on_close,
      on_message = self.on_message
    )
    self.is_resuming : bool = True
    self.connect()

  def reconnect(
    self
  ) -> None:
    """
    Creates a new connection using the cached URL if the app cannot resume
    """

    self.connection.close()
    self.connection : WebSocketApp = WebSocketApp(
      self.gateway,
      on_open    = self.on_open,
      on_error   = self.on_error,
      on_close   = self.on_close,
      on_message = self.on_message
    )
    self.connect()

  def on_open(
    self,
    ws : Self
  ) -> None:
    """
    Called when is successfully connected to the websocket

    Parameters
    ----------
    ws : DiscordWebSocket
    """

    if self.app.logger and self.app.logger.debug_mode: self.app.logger.debug(f"Connection opened with: {self.gateway}")
    if self.app.logger: self.app.logger.info("Connected to Gateway")


  def on_close(
    self,
    ws          : Self,
    status_code : int,
    message
  ) -> None:
    """
    Called when the connection is closed

    Parameters
    ----------
    message : str
      Message received from the closed connection

    status_code : int
      Status code of the connection closing

    ws : DiscordWebSocket
    """

    if self.app.logger: self.app.logger.warn(f"{ws}\n{status_code}\n{loads(message.content)}")


  def on_error(
    self,
    ws    : Self,
    error : Exception
  ) -> None:
    """
    Called when an error is catched

    Parameters
    ----------
    error : Exception
      Catched exception

    ws : DiscordWebSocket
    """
    if self.app.logger: self.app.logger.error(error)


  def send_heartbeat(
    self,
    jitter : bool = False,
    wait   : bool = True
  ) -> None:
    """
    Send a heartbeat

    Parameters
    ----------
    jitter : bool
      Whether to jitter the delay. Jittered delay is calculated by ` heartbeat_interval * random() `. Defaults to ` False `

    wait : bool
      Whether to delay the heartbeat. Defaults to ` True `
    """

    wait_time : int = self.heartbeat_interval
    if jitter: wait_time *= random()
    if wait: asyncio.run(
        asyncio.sleep(
          wait_time / 1_000
        )
      )
    self.send(
      Payload(
        op = PayloadType.HeartBeat,
        d  = self.last_sequence
      )
    )
    if self.app.logger and self.app.logger.debug_mode: self.app.logger.debug("Heartbeat sent successfully")


  def setup_ready(
    self,
    payload : Payload
  ) -> None:
    """
    Called after receiving the READY gateway event and before calling the on_ready event listeners

    Parameters
    ----------
    payload : Payload
      Payload object of the READY gateway event
    """

    user                          : User    = User.from_data(payload.d["user"])
    self.app.user                 : User    = user
    self.__resume_gateway_url     : str     = payload.d["resume_gateway_url"]
    self.__session_id             : str     = payload.d["session_id"]
    self.app._relationships       : list    = payload.d["relationships"]
    self.app._private_channels    : list    = payload.d["private_channels"]
    self.app._presences           : list    = payload.d["presences"]
    self.app._guild_join_requests : list    = payload.d["guild_join_requests"]
    self.app._appinfo             : AppInfo = AppInfo.from_data(payload.d["application"])
    Thread(
      target = asyncio.run,
      args   = [
        self.app._App__app_events.call(payload.t)
      ]
    ).start()


  def on_message(
    self,
    ws      : Self,
    message
  ) -> None:
    """
    Called when a message is received from the connection

    Parameters
    ----------
    message
      Message received
    
    ws : DiscordWebSocket
      Websocket that received the message
    """

    try:
      if self.app.logger and self.app.logger.debug_mode: self.app.logger.debug(f"received : {loads(message)}")
      payload : Payload = Payload.from_data(loads(message))

      match payload.op:
        case PayloadType.Hello:
          if self.app.logger and self.app.logger.debug_mode: self.app.logger.debug("Received Hello event")
          self.heartbeat_interval : int = payload.d["heartbeat_interval"]
          Thread(
            target = self.send_heartbeat,
            kwargs = {
              "jitter": True
            }
          ).start()

        case PayloadType.HeartBeatACK:
          if self.app.logger and self.app.logger.debug_mode: self.app.logger.debug("Received Heartbeat ACK")
          if not self.identify_sent and not self.is_resuming:
            Thread(
              target = self.identify
            ).start()
          Thread(
            target = self.send_heartbeat
          ).start()

        case PayloadType.HeartBeat:
          Thread(
            target = self.send_heartbeat
          ).start()

        case PayloadType.Reconnect:
          if payload.d: self.resume()
          else: self.reconnect()

        case PayloadType.Dispatch:
          self.last_sequence : Optional[int] = payload.s
          match payload.t:
            case GatewayEvents.Ready:
              if self.app.logger and self.app.logger.debug_mode: self.app.logger.debug("Received READY event")
              Thread(
                target = self.setup_ready,
                args   = [
                  payload
                ]
              ).start()

            case GatewayEvents.GuildCreate:
              if self.app.logger and self.app.logger.debug_mode: self.app.logger.debug("Received GUILD_CREATE event")
              guild = Guild.from_data(self, payload.d)
              Thread(
                target = asyncio.run,
                args   = [
                  self.app._App__app_events.call(
                    payload.t,
                    guild = guild
                  )
                ]
              ).start()

            case GatewayEvents.Resumed:
              if self.app.logger and self.app.logger.debug_mode: self.app.logger.debug("Connection resumed")
    except Exception as error:
      if self.app.logger: return self.app.logger.error(error)