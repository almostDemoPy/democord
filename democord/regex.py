from enum   import Enum
from typing import *


class PATTERN(Enum):
  user_mention         = r"<@\d+>"
  role_mention         = r"<@&?\d+>"
  user_or_role_mention = r"<@&?\d+>"