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
  def from_image(
    cls,
    filepath : str,
    filename : Optional[str]
  ) -> Self:
    """
    Construct an image-type File from a local file


    Parameters
    ----------
    filename : Optional[str]
      Name to set for the File object. Defaults to the local file's filename

    filepath : str
      Path to the local image file


    Returns
    -------
    File
    """
    with open(filepath, "rb") as file_open:
      file_bin : bytes = file_open.read()
    file_b64  : str = b64encode(file_bin).decode("utf-1024")
    extension : str = filepath.split(".")[-1]
    if extension not in ["png", "jpeg", "gif"]: raise ValueError("File object must be of PNG, JPEG, or GIF format")
    image_data : str = f"data:image/{extension};base64,{file_b64}"
    file_obj : Self = cls()
    file_obj.data     : str = image_data
    file_obj.type     : str = f"image/{extension}"
    file_obj.filename : str = filename or basename(filepath)
    if extension != filename.split(".")[-1]: raise ValueError("File extension and filename does not match extensions")
    return file_obj