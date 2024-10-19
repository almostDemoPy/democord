from .asset       import Asset
from .channels    import (
                         TextChannel
                         )
from .enums       import (
                         ChannelType,
                         ForumLayout,
                         ForumSortOrder
                         )
from .flags       import ChannelFlags
from .member      import Member
from .permissions import PermissionOverwrites
from .user        import User
from datetime     import datetime
from typing       import *

if TYPE_CHECKING:
  from .ws     import DiscordWebSocket


class Constructor:
  ws : DiscordWebSocket = None

  @staticmethod
  def channel(data : Dict[str, Any]) -> Union[TextChannel]:
    try:
      channel_classes : Dict[ChannelType, GuildChannel] = {
        ChannelType.text : TextChannel
      }
      channel : GuildChannel = channel_classes[ChannelType(data["type"])]()
      channel.__dict__["ws"] : DiscordWebSocket = Constructor.ws
      for attribute in data:
        match attribute:
          case "application_id":
            channel.__dict__[attribute] : int = int(data[attribute])
          case "applied_tags":
            channel.__dict__[attribute] : List[ForumTag] = [Constructor.forum_tag([tag_data for tag_data in data["available_tags"] if int(tag_data["id"]) == int(tag_id)][0]) for tag_id in data[attribute]]
          case "available_tags":
            # implement: ForumTag
            # implement: Constructor.forum_tag()
            channel.__dict__[attribute] : List[ForumTag] = [Constructor.forum_tag(tag_data) for tag_data in data[attribute]]
          case "bitrate":
            channel.__dict__[attribute] : int = data[attribute]
          case "default_auto_archive_duration":
            channel.__dict__["auto_archive_duration"] : int = data[attribute]
          case "default_forum_layout":
            channel.__dict__[attribute] : Optional[ForumLayout] = ForumLayout(data[attribute]) if data[attribute] != 0 else None
          case "default_reaction_emoji":
            # implement: Emoji
            # implement: Constructor.emoji()
            channel.__dict__[attribute] : Optional[Emoji] = Constructor.emoji(data[attribute]) if data[attribute] else None
          case "default_sort_order":
            channel.__dict__[attribute] : Optional[ForumSortOrder] = ForumSortOrder(data[attribute]) if data[attribute] else None
          case "default_thread_rate_limit_per_user":
            channel.__dict__["default_thread_slowmode"] : int = data[attribute]
          case "flags":
            channel.__dict__[attribute] : List[ChannelFlags] = [flag for flag in ChannelFlags if ((data[attribute] & flag.value) == flag.value)]
          case "guild_id":
            channel.__dict__["guild"] : Guild = Constructor.ws.app.guilds(id = int(data[attribute]))
          case "icon":
            # implement: Constructor.asset()
            channel.__dict__[attribute] : Asset = None
          case "id":
            channel.__dict__[attribute] : int = int(data[attribute])
          case "last_message_id":
            channel.__dict__[attribute] : Optional[int] = int(data[attribute])
          case "last_pin_timestamp":
            channel.__dict__["last_pin"] : Optional[datetime] = datetime.fromtimestamp(data[attribute]) if data[attribute] else None
          case "managed":
            channel.__dict__[attribute] : bool = data[attribute]
          case "member":
            # implement Constructor.member()
            channel.__dict__[attribute] : Member = None
          case "member_count":
            channel.__dict__[attribute] : int = data[attribute]
          case "message_count":
            channel.__dict__[attribute] : int = data[attribute]
          case "name":
            channel.__dict__[attribute] : Optional[str] = data[attribute]
          case "nsfw":
            channel.__dict__[attribute] : bool = data[attribute]
          case "owner_id":
            channel.__dict__[attribute] : int = int(data[attribute])
          case "parent_id":
            # implement: get channel endpoint
            channel.__dict__["parent"] : Optional[CategoryChannel] = Constructor.channel(Constructor.ws.get(GET.guild_channel(int(data["guild_id"]), int(data[attribute])))) if data[attribute] else None
          case "permissions":
            # incomplete analysis
            channel.__dict__[attribute] : Permissions = None
          case "permission_overwrites":
            channel.__dict__["overwrites"] : PermissionOverwrites = PermissionOverwrites.from_data(data[attribute])
          case "position":
            channel.__dict__[attribute] : int = data[attribute]
          case "rate_limit_per_user":
            channel.__dict__["slowmode"] : int = data[attribute]
          case "recipients":
            channel.__dict__[attribute] : List[User] = [User.from_data(user_data) for user_data in data[attribute]]
          case "rtc_region":
            channel.__dict__[attribute] : Optional[str] = data[attribute]
          case "thread_metadata":
            # implement: Constructor.thread_metadata()
            # implement: ThreadMetadata
            channel.__dict__[attribute] = None
          case "topic":
            channel.__dict__[attribute] : Optional[str] = data[attribute]
          case "total_message_sent":
            channel.__dict__[attribute] : int = data[attribute]
          case "user_limit":
            channel.__dict__[attribute] : int = data[attribute]
          case "video_quality_mode":
            channel.__dict__[attribute] : int = data[attribute]
      return channel
    except Exception as error:
      if ws.app.logger: ws.app.logger.error(error)