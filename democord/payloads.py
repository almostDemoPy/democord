from .enums import (
  PayloadType,
  GatewayEvents
)
from typing import (
  Self
)


class Payload:
  def __init__(
    self,
    *,
    op : PayloadType,
    d : dict | int | None = None,
    t : int | None = None,
    s : int | None = None
  ) -> None:
    self.op : PayloadType = op
    self.d : dict | int = d
    self.t : int | None = t
    self.s : int | None = s


  def __str__(self) -> str:
    return f"Payload(t = {self.t} , s = {self.s} , op = {self.op} , d = {self.d})"


  def to_json(self) -> dict:
    return {
      "t"  : self.t,
      "s"  : self.s,
      "op" : self.op.value,
      "d"  : self.d
    }


  @classmethod
  def identify(cls, **kwargs) -> Self:
    d : dict = {
      "token"           : kwargs["token"],
      "properties"      : {
        "os"            : "linux",
        "browser"       : "democord",
        "device"        : "democord"
      },
      "intents"         : kwargs.get("intents", 0)
    }
    if kwargs.get("compress"): d["compress"] = kwargs["compress"]
    if kwargs.get("large_threshold"): d["large_threshold"] = kwargs["large_threshold"]
    if kwargs.get("shard"): d["shard"] = kwargs["shard"]
    if kwargs.get("presence"): d["presence"] = kwargs["presence"]
    return cls(
      op = PayloadType.Identify,
      d = d
    )

  
  @classmethod
  def from_data(cls, data : dict, **kwargs) -> Self:
    match data["op"]:
      case 0:
        match data["t"]:
          case "READY": t = GatewayEvents.Ready
          case "GUILD_CREATE": t = GatewayEvents.GuildCreate
        return cls(
          op = PayloadType.Dispatch,
          t = t,
          s = data["s"],
          d = data["d"]
        )
      case 1:
        return cls(
          op = PayloadType.HeartBeat
        )
      case 10:
        return cls(
          op = PayloadType.Hello,
          d = data["d"]
        )
      case 11:
        return cls(
          op = PayloadType.HeartBeatACK
        )