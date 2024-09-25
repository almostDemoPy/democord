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