# backend/app/rules/content/equation_reference_rule.py

import re

from backend.app.models.document import (
    DocumentModel
)

from backend.app.models.validation import (
    ValidationError
)

from backend.app.rules.base_rule import (
    BaseRule
)

from backend.app.config.semantic_types import (
    EQUATION
)


class EquationReferenceRule(BaseRule):

    """
    Проверяет ссылки на формулы:

    см. формулу 1
    в формуле 2
    по формуле 3
    как показано в формуле 4
    """

    EQUATION_NUMBER_PATTERN = re.compile(
        r"\((\d+)\)"
    )

    EQUATION_REFERENCE_PATTERN = re.compile(
        r"(формул[аыееи]?|equation|formula)\s+(\d+)",
        re.IGNORECASE
    )

    def check(
        self,
        document: DocumentModel
    ) -> list[ValidationError]:

        errors = []

        existing_equations = set()

        # -----------------------------------------
        # Собираем все существующие формулы
        # -----------------------------------------

        for paragraph in (
            document.paragraphs
        ):

            if (
                paragraph.semantic_type
                != EQUATION
            ):

                continue

            match = (
                self.EQUATION_NUMBER_PATTERN.search(
                    paragraph.text
                )
            )

            if not match:
                continue

            equation_number = int(
                match.group(1)
            )

            existing_equations.add(
                equation_number
            )

        # -----------------------------------------
        # Проверяем ссылки в тексте
        # -----------------------------------------

        for paragraph in (
            document.paragraphs
        ):

            # сами формулы пропускаем

            if (
                paragraph.semantic_type
                == EQUATION
            ):

                continue

            text = (
                paragraph.text
            )

            references = (
                self.EQUATION_REFERENCE_PATTERN.findall(
                    text
                )
            )

            # -------------------------------------
            # Проверяем каждую ссылку
            # -------------------------------------

            for (
                _,
                number
            ) in references:

                try:

                    equation_number = int(
                        number
                    )

                except ValueError:

                    errors.append(
                        ValidationError(
                            category="equation",

                            message=(
                                "Некорректная ссылка на формулу"
                            ),

                            expected=(
                                "Целый номер формулы"
                            ),

                            actual=number,

                            paragraph_index=(
                                paragraph.paragraph_index
                            )
                        )
                    )

                    continue

                # ---------------------------------
                # Формулы не существует
                # ---------------------------------

                if (
                    equation_number
                    not in existing_equations
                ):

                    errors.append(
                        ValidationError(
                            category="equation",

                            message=(
                                "Указана ссылка на несуществующую формулу"
                            ),

                            expected=(
                                "Существующий номер формулы"
                            ),

                            actual=str(
                                equation_number
                            ),

                            paragraph_index=(
                                paragraph.paragraph_index
                            )
                        )
                    )

        return errors