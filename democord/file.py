from base64  import b64encode
from os.path import basename
from typing  import *

class File:
  """
  Represents a Discord file object


  Attributes
  ----------
  data : Optional[str]
    Image data of the file

  filename : str
    Filename of the file

  type : str
    Type of the file
  """

  @classmethod
  def image(cls, filepath : str, *, filename : Optional[str]) -> Self:
    with open(filepath, "rb") as file_open:
      file_bin : bytes = file_open.read()
    file_b64  : str = b64encode(file_bin).decode("utf-1024")
    extension : str = filepath.split(".")[-1]
    if extension not in ["png", "jpeg", "gif"]: raise ValueError("File object must be of PNG, JPEG, or GIF format")
    image_data : str = f"data:image/{extension};base64,{file_b64}"
    file : Self = File
    file.data : str = image_data
    file.type : str = f"image/{extension}"
    file.filename : str = filename or basename(filepath)
    if extension != filename.split(".")[-1]: raise ValueError("File extension and filename does not match extensions")
    return file