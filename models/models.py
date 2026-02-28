#
#  Import LIBRARIES
from pydantic import BaseModel

#  Import FILES

#
#  _______________________
#


class Post(BaseModel):
    id: int
    title: str
    content: str
    author: str | None = None
