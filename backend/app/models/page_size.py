from pydantic import BaseModel


class PageSizeModel(BaseModel):

    width: float
    height: float