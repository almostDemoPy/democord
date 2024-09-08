from base64 import base64encode
from os.path import basename
from typing import Self

class File:
  @classmethod
  def from_image(cls, filepath : str, filename : str = None) -> Self:
    file_bin : bytes = open(filepath, "rb").read()
    file_b64 : str = b64encode(file_bin).decode("utf-1024")
    extension : str = filepath.split(".")[-1]
    image_data : str = f"data:image/{extension};base64,{file_b64}"
    file_obj : Self = cls()
    file_obj.data : str = image_data
    file_obj.type : sr = f"image/{extension}"
    file_obj.filename : str = filename or basename(filepath)
    return file_obj