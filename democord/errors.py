from .enums import PermissionFlags
from typing import *


class APILimit(Exception): ...

class BotMissingPermissions(Exception):
  def __str__(self) -> str:
    return ", ".join(
      [
        permission.name
        for permission in self.missing_permissions
      ]
    )


class MissingPermissions(Exception):
  def __str__(self) -> str:
    return ", ".join([permission.name for permission in self.missing_permissions])