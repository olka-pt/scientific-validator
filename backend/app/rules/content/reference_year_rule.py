# backend/app/rules/content/reference_year_rule.py

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


class ReferenceYearRule(BaseRule):

    YEAR_PATTERN = re.compile(
        r"(19\d{2}|20\d{2})"
    )

    CURRENT_YEAR = 2026

    MAX_SOURCE_AGE = 15

    MIN_MODERN_PERCENT = 50

    MODERN_SOURCE_AGE = 5

    def check(
        self,
        document: DocumentModel
    ) -> list[ValidationError]:

        errors = []

        reference_paragraphs = []

        for paragraph in (
            document.paragraphs
        ):

            if (
                paragraph.semantic_type
                == "reference_item"
            ):

                reference_paragraphs.append(
                    paragraph
                )

        if not reference_paragraphs:

            return errors

        total_sources = len(
            reference_paragraphs
        )

        modern_sources = 0

        for paragraph in (
            reference_paragraphs
        ):

            text = paragraph.text

            found_years = re.findall(
                self.YEAR_PATTERN,
                text
            )

            if not found_years:

                errors.append(
                    ValidationError(
                        category="references",

                        message=(
                            "Год публикации не найден"
                        ),

                        expected=(
                            "од, например 2024"
                        ),

                        actual=text[:80],

                        paragraph_index=(
                            paragraph.paragraph_index
                        )
                    )
                )

                continue

            year = int(
                found_years[-1]
            )

            age = (
                self.CURRENT_YEAR
                - year
            )

            # Слишком старый источник

            if (
                age
                > self.MAX_SOURCE_AGE
            ):

                errors.append(
                    ValidationError(
                        category="references",

                        message=(
                            "Источник слишком старый"
                        ),

                        expected=(
                            f"Не старше "
                            f"{self.MAX_SOURCE_AGE} лет"
                        ),

                        actual=str(year),

                        paragraph_index=(
                            paragraph.paragraph_index
                        )
                    )
                )

            # Современный источник

            if (
                age
                <= self.MODERN_SOURCE_AGE
            ):

                modern_sources += 1

        modern_percent = (
            modern_sources
            / total_sources
        ) * 100

        if (
            modern_percent
            < self.MIN_MODERN_PERCENT
        ):

            errors.append(
                ValidationError(
                    category="references",

                    message=(
                        "Недостаточно современных источников"
                    ),

                    expected=(
                        f">= "
                        f"{self.MIN_MODERN_PERCENT}%"
                    ),

                    actual=(
                        f"{modern_percent:.1f}%"
                    ),

                    paragraph_index=-1
                )
            )

        return errors