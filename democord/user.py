class User:
  def __init__(
    self,
    data : dict[str, str | bool | int | dict | None]
  ) -> None:
    print(data)
    for attribute in data:
      self.__dict__[attribute] = data[attribute]


  def __getattribute__(self, attribute : str) -> str | int | bool | None:
    match attribute:
      case "id" | "discriminator": return int(super().__getattribute__(attribute))
      case "global name":
        global_name : str | None = super().__getattribute__(attribute)
        if not global_name: global_name : str = self.username
        return global_name
      case _: return super().__getattribute__(attribute)


  def __getattr__(self, attribute : str) -> None:
    raise AttributeError(f"User object has no attribute: {attribute}")


  @classmethod
  def from_data(cls, data : dict) -> None:
    return cls(data)