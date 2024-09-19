from .enums import PermissionFlags
from typing import *


class MissingPermissions(Exception):
  def __init__(
    self,
    *missing_permissions : PermissionFlags
  ) -> None:
    self.missing_permissions : List[PermissionFlags] = list(missing_permissions)

  def __str__(self) -> str:
    return f"You are lacking {len(self.missing_permissions):,} permission(s) to perform this action:\n{"\n".join([f"- {permission.name}" for permission in self.missing_permissions])}"