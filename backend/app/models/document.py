from pydantic import BaseModel

from backend.app.models.paragraph import ParagraphModel
from backend.app.models.page_margins import PageMarginsModel
from backend.app.models.page_size import PageSizeModel
from backend.app.models.table import TableModel


class DocumentModel(BaseModel):

    paragraphs: list[ParagraphModel]

    margins: PageMarginsModel

    page_size: PageSizeModel

    tables: list[TableModel] = []

    page_count: int | None = None

    has_page_numbering: bool = False