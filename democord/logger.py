from datetime import (
  datetime,
  timedelta
)

class Logger:
  def __init__(
    self,
    *,
    _format : str = "%Y-%m-%d %H:%M:%S"
  ) -> None:
    self._format : str = _format

  def info(self, message : str) -> None:
    current_time : datetime = datetime.now()
    print(f"[ {current_time.strftime(self._format)} ] INFO | {message}".replace("\n", f"\n{" " * (len(current_time.strftime(self._format)) + 10)}| "))