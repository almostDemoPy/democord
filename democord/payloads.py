from .types import (
  PayloadType
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
    return cls(
      op = PayloadType.Identify,
      d = {
        "token"           : kwargs["token"],
        "properties"      : {
          "os"            : "linux",
          "browser"       : "democord",
          "device"        : "democord"
        },
        "compress"        : kwargs.get("compress", False),
        "large_threshold" : kwargs.get("large_threshold", 50),
        "shard"           : kwargs.get("shard", None),
        "presence"        : kwargs.get("presence", None),
        "intents"         : kwargs.get("intents", 0)
      }
    )

  
  @classmethod
  def from_data(cls, data : dict, **kwargs) -> Self:
    match data["op"]:
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