from .channels import VoiceChannel
from .reqs import PATCH
from .role import Role
from .user  import User
from typing import *


class Member:
  """
  Represents a Discord guild member


  Attributes
  ----------
  nick : Optional[str]
    The set nickname of the member. If none, defaults to the member's username instead

  user : Optional[user]
    Corresponding User object of the member
  """

  @property
  def id(
    self
  ) -> int:
    """
    Returns the ID of the member


    Returns
    -------
    int
    """

    return self.user.id

  async def edit(
    self,
    **attributes
  ) -> Member:
    try:
      data : Dict[str, Any] = {}
      reason : Optional[str] = None
      for attribute in attributes:
        match attribute:
          case "nick":
            if not isinstance(attributes[attribute], str): raise TypeError("nick: must be of type <str>")
            # check permission: manage_nicknames
            data[attribute] : str = attributes[attribute]
          case "roles":
            if isinstance(attributes[attribute], list):
              for role in attributes[attribute]:
                if not isinstance(role, Role): raise ValueError("roles: must contain <Role> objects")
              # check permission: manage_roles
              data[attribute] : List[Role] = [role.id for role in attributes[attribute]]
              data[attribute] += [role.id for role in self.roles if role not in data[attribute]]
            else: raise TypeError("roles: must be of type <list> containing <Role> objects")
          case "mute":
            if not isinstance(attributes[attribute], bool): raise TypeError("mute: must be of type <bool>")
            # check permission: mute_members
            data[attribute] : bool = attributes[attribute]
          case "deaf":
            if not isinstance(attributes[attribute], bool): raise TypeError("deaf: must be of type <bool>")
            # check permission: deafen_members
            data[attribute] : bool = attributes[attribute]
          case "voice_channel":
            if not isinstance(attributes[attribute], VoiceChannel): raise TypeError("voice_channel: must be of type <VoiceChannel>")
            # check permission: move_members
            data[attribute] : int = attributes[attribute].id
          case "reason":
            if not isinstance(attributes[attribute], str): raise TypeError("reason: must be of type <str>")
            reason : Optional[str] = reason
      response : Dict[str, Any] = self.ws.patch(
        PATCH.member(self.guild.id, self.id),
        data = data,
        reason = reason
      )
      self : Self = Member.from_data(self.ws, response)
      return self
    except Exception as error:
      if self.ws.app.logger: self.ws.app.logger.error(error)

  @classmethod
  def from_data(
    cls,
    data : Dict[str, Any]
  ) -> Self:
    """
    Construct a Member object from a dictionary payload


    Parameters
    ----------
    data : Dict[str, Any]
      Dictionary payload of a Member object


    Returns
    -------
    Member
    """

    member : Self = cls()
    for attribute in data:
      match attribute:
        case "user": member.__dict__[attribute] : User = User.from_data(data[attribute])
        case "nick": member.__dict__[attribute] : str  = data[attribute]
    return member