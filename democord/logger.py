from colorama  import (
                      Fore,
                      Style
                      )
from datetime  import (
                      datetime,
                      timedelta
                      )
from traceback import (
                      FrameSummary,
                      TracebackException
                      )
from typing    import *


class Logger:
  """
  Custom logger used for the library


  Attributes
  ----------
  _format : str
    String format for displaying date and time

  debug_mode : bool
    Whether the logger is in debug mode or not
  """

  def __init__(
    self,
    *,
    debug_mode  : bool = False,
    time_format : str  = "%Y-%m-%d %H:%M:%S"
  ) -> None:
    """
    Construct a Logger instance


    Parameters
    ----------
    debug_mode : bool
      Whether to enable debug mode for the logger

    time_format : Optional[str]
      The string format to use for displaying date and time. Defaults to ` %Y-%m-%d %H:%M:%S `
    """

    self._format         : str  = time_format
    self.max_type_length : int  = 7
    self.debug_mode      : bool = debug_mode

  def debug(
    self,
    message : str
  ) -> None:
    """
    Sends a DEBUG log. This can only be done if Logger.debug_mode is enabled


    Parameters
    ----------
    message : str
      Message string for the log
    """

    if not self.debug_mode: return self.error("DEBUG_MODE is not enabled for this logger")
    self._log(
      log_type = "DEBUG",
      message  = str(message)
    )

  def error(
    self,
    exception : Exception
  ) -> None:
    """
    Sends an ERROR exception according to the exception


    Parameters
    ----------
    exception : Exception
      The exception to log
    """

    tbexc : TracebackException = TracebackException.from_exception(exception)
    frame : FrameSummary       = tbexc.stack[0]
    self._log(
      log_type = "ERROR",
      message  = f"{frame.filename} - Line {frame.lineno:,}\n{frame.line}\n{tbexc.exc_type.__name__}: {tbexc}"
    )

  def info(
    self, 
    message : str
  ) -> None:
    """
    Sends an INFO log


    Parameters
    ----------
    message : str
      Message string for the log
    """

    self._log(
      log_type = "INFO",
      message  = str(message)
    )

  def warn(
    self,
    message : str
  ) -> None:
    """
    Sends a WARNING log
    

    Returns
    -------
    message : str
      Message string for the log
    """

    self._log(
      log_type = "WARNING",
      message  = str(message)
    )

  def _log(
    self,
    *, 
    log_type : str, 
    message  : str
  ) -> None:
    """
    Sends the log message


    Parameters
    ----------
    log_type : str
      Type of log to print

    message : str
      The string of message to log
    """

    log_colors : Dict[str, str] = {
      "INFO"   : Fore.CYAN,
      "ERROR"  : Fore.RED,
      "WARNING": Fore.YELLOW,
      "DEBUG"  : Fore.YELLOW
    }
    timestamp : str = datetime.now().strftime(self._format)
    message   : str = message.replace("\n", f"\n{" " * (len(timestamp) + 13)}| ")
    print(f"[ {timestamp} ] {log_colors[log_type]}{"{0:>{1}}".format(log_type, self.max_type_length)}{Style.RESET_ALL} | {message}")