from base64 import base64encode
from typing import Self

class File:
  @classmethod
  def from_file(cls, filepath : str) -> Self:
    file_bin : bytes = open(filepath, "rb").read()
    file_b64 : str = b64encode(file_bin).decode("utf-8")
    extension : str = filepath.split(".")[-1]
    image_data : str = f"data:image/{extension};base64,{file_b64}"
    file_obj : Self = cls()
    file_obj.data : str = image_data
    file_obj.type : sr = f"image/{extension}"
    return file_obj