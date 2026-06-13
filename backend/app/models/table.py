from pydantic import BaseModel


class TableCellModel(BaseModel):

    text: str

    font_size: float | None = None


class TableRowModel(BaseModel):

    cells: list[TableCellModel]


class TableModel(BaseModel):

    rows: list[TableRowModel]

    table_index: int