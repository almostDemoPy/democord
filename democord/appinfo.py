from .flags import  (
                    ApplicationFlags
                    )
from typing import *


class AppInfoFlags(int):
  """
  Callable property for AppInfo.flags
  """

  def __call__(self) -> List[str]:
    """
    Returns the application's flags in strings of names

    Returns
    -------
    List[str]
    """
    return [
      name
      for name, flag in ApplicationFlags._member_map_.items()
      if ( self & flag.value ) == flag.value
    ]

  def __int__(self) -> int:
    """
    The bitfield value of the application's flags
    """
    return self


class AppInfo:
  """
  The application's info data


  Attributes
  ----------
  approximate_guild_count : Optional[int]
    Approximate count of guilds the bot is added to

  approximate_user_install_count : Optional[int]
    Approximate count of users that installed the application

  bot : Optional[User]
    User object of the application

  cover_image : Optional[Asset]
    Applicaiton's default rich presence invite

  custom_install_url : Optional[str]
    Default custom authorization URL for the application

  description : str
    Description of the application

  flags : Union[int, List[str]]
    The application's flag info

  guild : Optional[Guild]
    The guild associated with the app.

  icon : Optional[Asset]
    Set icon for the application

  id : int
    Application ID

  install_params : Optional[Dict[str, List[str]]]
    Set install parameters for the application's default in-app authorization link

  integration_types_config : Optional[Tuple[IntegrationType]]
    Set integration types for the application

  interactions_endpoint_url : Optional[str]
    Interactions endpoint URL for the application

  name : str
    Name of the application

  owner : Optional[User]
    The application's owner

  primary_sku_id : Optional[int]
    The ID of the "Game SKU" that is created, if exists

  privacy_policy_url : Optional[str]
    URL of the application's Privacy Policy

  public : bool
    Whether the bot can be added by anyone or only the application owner

  redirect_uris : Optional[List[str]]
    Redirect URIs for the application

  require_code_grant : bool
    Whether the bot requires OAuth2 Code grant when adding

  role_connections_verification_url : Optional[str]
    Role connections verification URL for the application

  slug : Optional[str]
    The URL slug that links to the store page

  tags : Optional[List[str]]
    List of tags describing the application

  team : Optional[Team]
    The Team object the application belongs in

  tos_url : Optional[str]
    URL of the application's Terms of Service

  verify_key : str
    Hex encoded key for verification in interactions and the GameSDK's GetTicket
  """


  def __getattribute__(
    self,
    attribute : str
  ) -> Any:
    """
    Returns an attribute, if exists

    Returns
    -------
    Any
    """

    match attribute:
      case "id": return int(self.__dict__["id"])
      case _   : return super().__getattribute__(attribute)


  def __contains__(
    self,
    name : str
  ) -> bool:
    """
    Checks whether an application flag exists in AppInfo.flags attribute

    Returns
    -------
    bool
    """

    flag : ApplicationFlags = ApplicationFlags._member_map_.get(name)
    if not flag: raise AttributeError(f"There is no such Application Flag named: {name}")
    return ( self.value & flag.value ) == flag.value


  @property
  def value(self) -> int:
    """
    Returns the bitfield flag value

    Returns
    -------
    int
    """
    return self._flags_value