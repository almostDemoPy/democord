from .enums import (
                   GatewayEvents,
                   PayloadType
                   )
from typing import *


class Payload:
  """
  Represents a received or sent gateway payload


  Attributes
  ----------
  op : PayloadType
    Type of received or sent payload

  d : Optional[Union[Dict[str, Any], int]]
    ` d ` field of a payload, if any

  t : Optional[str]
    ` t ` field of a payload

  s : Optional[int]
    Sequence number
  """

  def __init__(
    self,
    *,
    op : PayloadType,
    d  : Optional[Union[Dict[str, Any], int]] = None,
    t  : Optional[str]                        = None,
    s  : Optional[int]                        = None
  ) -> None:
    self.op : PayloadType                = op
    self.d  : Union[Dict[str, Any], int] = d
    self.t  : Optional[int]              = t
    self.s  : Optional[int]              = s


  def __str__(
    self
  ) -> str:
    """
    Return a human-readable string representation of the payload object


    Returns
    -------
    str
    """
    
    return f"Payload(t = {self.t} , s = {self.s} , op = {self.op} , d = {self.d})"


  def to_json(
    self
  ) -> Dict[str, Any]:
    """
    Convert a Payload object into a dictionary


    Returns
    -------
    Dict[str, Any]
    """

    return {
      "t"  : self.t,
      "s"  : self.s,
      "op" : self.op.value,
      "d"  : self.d
    }


  @classmethod
  def identify(
    cls,
    **kwargs
  ) -> Self:
    """
    Creates an Identify-type Payload object


    Parameters
    ----------
    compress : Optional[bool]
      Whether the connection supports compression of packets

    intents : int
      Bitfield intents value

    large_threshold : Optional[int]
      Value between 50 and 250, total number of members where the gateway will stop sending offline members in the guild member list

    presence : Optional[Activity]
      Initial presence structure

    shard : Optional[Tuple[int, int]]
      Used for guild sharding

    token : str
      Bot token


    Returns
    -------
    Payload
    """

    d : Dict[str, Union[Dict[str, str | int], str, int]] = {
      "token"           : kwargs["token"],
      "properties"      : {
        "os"            : "linux",
        "browser"       : "democord",
        "device"        : "democord"
      },
      "intents"         : kwargs.get("intents", 0)
    }
    if kwargs.get("compress"):        d["compress"]        : bool            = kwargs["compress"]
    if kwargs.get("large_threshold"): d["large_threshold"] : int             = kwargs["large_threshold"]
    if kwargs.get("presence"):        d["presence"]                          = kwargs["presence"]
    if kwargs.get("shard"):           d["shard"]           : Tuple[int, int] = kwargs["shard"]
    return cls(
      op = PayloadType.Identify,
      d  = d
    )

  
  @classmethod
  def from_data(
    cls,
    data : Dict[str, Any]
  ) -> Self:
    """
    Construct a Payload instance from a given dictionary payload data


    Parameters
    ----------
    data : Dict[str, Any]
      Dictionary payload data


    Returns
    -------
    Payload
    """

    match data["op"]:
      case 0:
        match data["t"]:
          case "READY":        t : GatewayEvents = GatewayEvents.Ready
          case "GUILD_CREATE": t : GatewayEvents = GatewayEvents.GuildCreate
          case _: t = data["t"]
        return cls(
          op = PayloadType.Dispatch,
          t  = t,
          s  = data["s"],
          d  = data["d"]
        )
      case 1:
        return cls(
          op = PayloadType.HeartBeat
        )
      case 7:
        return cls(
          op = PayloadType.Reconnect,
          d  = data["d"]
        )
      case 10:
        return cls(
          op = PayloadType.Hello,
          d  = data["d"]
        )
      case 11:
        return cls(
          op = PayloadType.HeartBeatACK
        )