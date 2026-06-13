from pydantic import BaseModel


class PageMarginsModel(BaseModel):

    top: float
    bottom: float

    left: float
    right: float