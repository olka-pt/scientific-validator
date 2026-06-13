from pydantic import BaseModel


class ParagraphModel(BaseModel):

    text: str

    font_family: str | None = None
    font_size: float | None = None

    bold: bool = False
    italic: bool = False

    alignment: str | None = None

    semantic_type: str = "unknown"

    line_spacing: float | None = None

    first_line_indent: float | None = None

    left_indent: float | None = None
    right_indent: float | None = None

    space_before: float | None = None
    space_after: float | None = None

    paragraph_index: int

    starts_new_page: bool = False    