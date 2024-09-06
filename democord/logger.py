from datetime import (
  datetime,
  timedelta
)

class Logger:
  def __init__(
    self
  ) -> None:
    self._format : str = "%Y-%m-%d %H:%M:%S.%f"