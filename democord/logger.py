from colorama import (
  Fore,
  Style
)
from datetime import (
  datetime,
  timedelta
)
from traceback import TracebackException

class Logger:
  def __init__(
    self,
    *,
    debug_mode : bool = False,
    time_format : str = "%Y-%m-%d %H:%M:%S"
  ) -> None:
    self._format : str = time_format
    self.max_type_length : int = 7
    self.debug_mode : bool = debug_mode

  def _log(self, *, log_type : str, message : str) -> None:
    log_colors : dict[str, str] = {
      "INFO"   : Fore.CYAN,
      "ERROR"  : Fore.RED,
      "WARNING": Fore.YELLOW,
      "DEBUG"  : Fore.YELLOW
    }
    timestamp = datetime.now().strftime(self._format)
    message : str = message.replace("\n", f"\n{" " * (len(timestamp) + 13)}| ")
    print(f"[ {timestamp} ] {log_colors[log_type]}{"{0:>{1}}".format(log_type, self.max_type_length)}{Style.RESET_ALL} | {message}")

  def info(self, message : str) -> None:
    self._log(
      log_type = "INFO",
      message = str(message)
    )

  def error(self, exception : Exception) -> None:
    tbexc = TracebackException.from_exception(exception)
    frame = tbexc.stack[0]
    self._log(
      log_type = "ERROR",
      message = f"{frame.filename} - Line {frame.lineno:,}\n{frame.line}\n{tbexc.exc_type.__name__}: {tbexc}"
    )

  def warn(self, message : str) -> None:
    self._log(
      log_type = "WARNING",
      message = str(message)
    )

  def debug(self, message : str) -> None:
    if not self.debug_mode: return self.error("DEBUG_MODE is not enabled for this logger")
    self._log(
      log_type = "DEBUG",
      message = str(message)
    )