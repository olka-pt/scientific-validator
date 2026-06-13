# backend/app/rules/content/equation_layout_rule.py

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


class EquationLayoutRule(BaseRule):

    """
    Проверяет:
    1. Есть ли номер формулы
    2. Находится ли номер справа
    3. Нет ли номера в начале строки
    4. Нет ли нескольких номеров
    """

    EQUATION_NUMBER_PATTERN = re.compile(
        r"\((\d+)\)"
    )

    def check(
        self,
        document: DocumentModel
    ) -> list[ValidationError]:

        errors = []

        for paragraph in (
            document.paragraphs
        ):

            if (
                paragraph.semantic_type
                != EQUATION
            ):

                continue

            text = (
                paragraph.text.strip()
            )

            matches = list(
                self.EQUATION_NUMBER_PATTERN.finditer(
                    text
                )
            )

            # -------------------------------------------------
            # Нет номера формулы
            # -------------------------------------------------

            if not matches:

                errors.append(
                    ValidationError(
                        category="equation",

                        message=(
                            "Отсутствует номер формулы"
                        ),

                        expected=(
                            "Формула с номером справа"
                        ),

                        actual=text,

                        paragraph_index=(
                            paragraph.paragraph_index
                        )
                    )
                )

                continue

            # -------------------------------------------------
            # Несколько номеров формулы
            # -------------------------------------------------

            if len(matches) > 1:

                errors.append(
                    ValidationError(
                        category="equation",

                        message=(
                            "Обнаружено несколько номеров формулы"
                        ),

                        expected=(
                            "Только один номер формулы"
                        ),

                        actual=text,

                        paragraph_index=(
                            paragraph.paragraph_index
                        )
                    )
                )

            match = matches[-1]

            number_start = (
                match.start()
            )

            number_end = (
                match.end()
            )

            # -------------------------------------------------
            # Номер в начале строки
            # -------------------------------------------------

            if number_start <= 2:

                errors.append(
                    ValidationError(
                        category="equation",

                        message=(
                            "Номер формулы не должен быть в начале"
                        ),

                        expected=(
                            "Номер справа"
                        ),

                        actual=text,

                        paragraph_index=(
                            paragraph.paragraph_index
                        )
                    )
                )

            # -------------------------------------------------
            # Номер не в конце строки
            # -------------------------------------------------

            tail = (
                text[number_end:]
                .strip()
            )

            if tail:

                errors.append(
                    ValidationError(
                        category="equation",

                        message=(
                            "Номер формулы должен быть в конце"
                        ),

                        expected=(
                            "Номер справа"
                        ),

                        actual=text,

                        paragraph_index=(
                            paragraph.paragraph_index
                        )
                    )
                )

            # -------------------------------------------------
            # Проверка центровки формулы
            # -------------------------------------------------

            if (
                paragraph.alignment
                != "center"
            ):

                errors.append(
                    ValidationError(
                        category="equation",

                        message=(
                            "Формула должна быть выровнена по центру"
                        ),

                        expected="По центру",

                        actual=str(
                            paragraph.alignment
                        ),

                        paragraph_index=(
                            paragraph.paragraph_index
                        )
                    )
                )

        return errors