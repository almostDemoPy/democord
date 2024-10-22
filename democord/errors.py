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


class Forbidden(Exception): ...


class MissingArguments(Exception):
  def __str__(self) -> str:
    return f"{self.message}: " + (", ".join(
      [
        argument
        for argument in self.missing_arguments
      ]
    ))


class MissingPermissions(Exception):
  def __str__(self) -> str:
    return ", ".join([permission.name for permission in self.missing_permissions])


class NotFound(Exception):
  def __str__(self) -> str:
    return ", ".join(self.missing)