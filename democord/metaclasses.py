from typing import *


class BasePayload(dict):
  def __getattribute__(self, key : str) -> Optional[Any]:
    if key in self: return self[key]
    return super().__getattribute__(key)


class ThreadMemberPayload(BasePayload):
  flags          : int            = None
  id             : str            = None
  join_timestamp : str            = None
  member         : Dict[str, Any] = None
  user_id        : str            = None