class CallableInt(int):
  def __init__(self, instance) -> None:
    self.instance = instance