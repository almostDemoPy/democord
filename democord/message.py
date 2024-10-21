from .constructor import Constructor
from .errors      import APILimit
from typing       import *


class Message:

  async def pin(self, reason : Optional[str] = None) -> None:
    try:
      # check permission: manage_messages
      if len(await self.channel.pins()) == 50:
        raise Constructor.exception(APILimit, message = "can only pin up to 50 messages")
      response : Dict[None] = self.ws.put(
        PUT.pin_message(self.channel.id, self.id),
        reason = reason
      )
    except Exception as error:
      if self.ws.app.logger: self.ws.app.logger.error(error)