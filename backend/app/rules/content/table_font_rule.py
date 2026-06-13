from backend.app.models.document import (
    DocumentModel
)

from backend.app.models.validation import (
    ValidationError
)

from backend.app.rules.base_rule import (
    BaseRule
)


class TableFontRule(BaseRule):

    MIN_FONT_SIZE = 10

    MAX_FONT_SIZE = 12

    def check(
        self,
        document: DocumentModel
    ) -> list[ValidationError]:

        errors = []

        for table in document.tables:

            for row_index, row in enumerate(
                table.rows
            ):

                for cell_index, cell in enumerate(
                    row.cells
                ):

                    if (
                        cell.font_size
                        is None
                    ):

                        continue

                    if (
                        cell.font_size
                        < self.MIN_FONT_SIZE
                        or cell.font_size
                        > self.MAX_FONT_SIZE
                    ):

                        errors.append(
                            ValidationError(
                                category="tables",

                                message=(
                                    "Некорректный размер шрифта в таблице"
                                ),

                                expected=(
                                    f"Размер шрифта {self.MIN_FONT_SIZE}–{self.MAX_FONT_SIZE} пт"
                                ),

                                actual=(
                                    f"{cell.font_size} пт"
                                ),

                                paragraph_index=-1
                            )
                        )

        return errors