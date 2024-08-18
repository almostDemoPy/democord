from typing import Self


class Intents:
  def __init__(
    self,
    guilds : bool = False,
    members : bool = False,
    moderation : bool = False,
    emojis_and_stickers : bool = False,
    webhooks : bool = False,
    integrations : bool = False,
    invites : bool = False,
    voice_states : bool = False,
    presences : bool = False,
    messages : bool = False,
    reactions : bool = False,
    typing : bool = False,
    direct_messages : bool = False,
    direct_message_reactions : bool = False,
    direct_message_typing : bool = False,
    message_content : bool = False,
    scheduled_events : bool = False,
    auto_moderation_configuration : bool = False,
    auto_moderation_execution : bool = False,
    guild_polls : bool = False,
    dm_polls : bool = False
  ) -> None:
    pass


  @classmethod
  async def none(cls) -> Self:
    return cls()