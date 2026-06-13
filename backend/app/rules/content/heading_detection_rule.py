# backend/app/rules/content/heading_detection_rule.py

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


class HeadingDetectionRule(BaseRule):

    MIN_FONT_SIZE = 14

    REQUIRED_ALIGNMENT = "center"

    REQUIRED_BOLD = True

    HEADING_NUMBER_PATTERN = re.compile(
        r"^\d+"
    )

    def check(
        self,
        document: DocumentModel
    ) -> list[ValidationError]:

        errors = []

        for paragraph in (
            document.paragraphs
        ):

            text = (
                paragraph.text.strip()
            )

            if not text:

                continue

            is_heading = (

                paragraph.bold
                == self.REQUIRED_BOLD

                and

                paragraph.alignment
                == self.REQUIRED_ALIGNMENT

                and

                paragraph.font_size
                is not None

                and

                paragraph.font_size
                >= self.MIN_FONT_SIZE
            )

            if not is_heading:

                continue

            paragraph.semantic_type = (
                "heading"
            )

            # Проверка:
            # heading не должен быть слишком коротким

            if len(text) < 3:

                errors.append(
                    ValidationError(
                        category="structure",

                        message=(
                            "Заголовок слишком короткий"
                        ),

                        expected=(
                            "Осмысленный заголовок"
                        ),

                        actual=text,

                        paragraph_index=(
                            paragraph.paragraph_index
                        )
                    )
                )

            # Проверка:
            # нет точки в конце

            if text.endswith("."):

                errors.append(
                    ValidationError(
                        category="structure",

                        message=(
                            "Заголовок не должен заканчиваться точкой"
                        ),

                        expected=(
                            "Заголовок без точки"
                        ),

                        actual=text,

                        paragraph_index=(
                            paragraph.paragraph_index
                        )
                    )
                )

            # Проверка numbering

            has_number = bool(
                self.HEADING_NUMBER_PATTERN.match(
                    text
                )
            )

            if has_number:

                first_number = (
                    text.split()[0]
                )

                cleaned_number = (
                    first_number.replace(".", "")
                )

                if not cleaned_number.isdigit():

                    errors.append(
                        ValidationError(
                            category="structure",

                            message=(
                                "Некорректная нумерация заголовка"
                            ),

                            expected=(
                                "Числовая нумерация заголовка"
                            ),

                            actual=text,

                            paragraph_index=(
                                paragraph.paragraph_index
                            )
                        )
                    )

        return errors