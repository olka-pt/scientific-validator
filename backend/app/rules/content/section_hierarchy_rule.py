# backend/app/rules/content/section_hierarchy_rule.py

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


class SectionHierarchyRule(BaseRule):

    HEADING_PATTERN = re.compile(
        r"^(\d+(?:\.\d+)*)"
    )

    def check(
        self,
        document: DocumentModel
    ) -> list[ValidationError]:

        errors = []

        previous_levels = None

        for paragraph in (
            document.paragraphs
        ):

            if (
                paragraph.semantic_type
                != "heading"
            ):

                continue

            text = (
                paragraph.text.strip()
            )

            match = (
                self.HEADING_PATTERN.match(
                    text
                )
            )

            if not match:

                continue

            heading_number = (
                match.group(1)
            )

            current_levels = [

                int(level)

                for level in (
                    heading_number.split(".")
                )
            ]

            # Первый heading

            if previous_levels is None:

                if current_levels != [1]:

                    errors.append(
                        ValidationError(
                            category="structure",

                            message=(
                                "Документ должен начинаться с раздела 1"
                            ),

                            expected="1",

                            actual=heading_number,

                            paragraph_index=(
                                paragraph.paragraph_index
                            )
                        )
                    )

                previous_levels = (
                    current_levels
                )

                continue

            validation_error = (
                self.validate_hierarchy(
                    previous_levels,
                    current_levels
                )
            )

            if validation_error:

                errors.append(
                    ValidationError(
                        category="structure",

                        message=(
                            validation_error[
                                "message"
                            ]
                        ),

                        expected=(
                            validation_error[
                                "expected"
                            ]
                        ),

                        actual=heading_number,

                        paragraph_index=(
                            paragraph.paragraph_index
                        )
                    )
                )

            previous_levels = (
                current_levels
            )

        return errors

    def validate_hierarchy(
        self,
        previous: list[int],
        current: list[int]
    ) -> dict | None:

        # CASE 1
        # Same level:
        # 1.1 -> 1.2

        if len(current) == len(previous):

            expected = (
                previous.copy()
            )

            expected[-1] += 1

            if current != expected:

                return {
                    "message": (
                        "Нарушена последовательность разделов одного уровня"
                    ),

                    "expected": (
                        ".".join(
                            map(
                                str,
                                expected
                            )
                        )
                    )
                }

            return None

        # CASE 2
        # Nested level:
        # 1 -> 1.1

        if len(current) == len(previous) + 1:

            parent = current[:-1]

            if parent != previous:

                return {
                    "message": (
                        "Неверная вложенность подраздела"
                    ),

                    "expected": (
                        ".".join(
                            map(
                                str,
                                previous
                            )
                        )
                    )
                }

            if current[-1] != 1:

                return {
                    "message": (
                        "Нумерация подраздела должна начинаться с 1"
                    ),

                    "expected": (
                        ".".join(
                            map(
                                str,
                                previous + [1]
                            )
                        )
                    )
                }

            return None

        # CASE 3
        # Rollback:
        # 1.2 -> 2

        if len(current) < len(previous):

            expected = (
                previous[
                    :len(current)
                ]
            )

            expected[-1] += 1

            if current != expected:

                return {
                    "message": (
                        "Неверный переход между уровнями разделов"
                    ),

                    "expected": (
                        ".".join(
                            map(
                                str,
                                expected
                            )
                        )
                    )
                }

            return None

        # CASE 4
        # Too deep jump:
        # 1 -> 1.1.1

        if len(current) > len(previous) + 1:

            return {
                "message": (
                    "Слишком большой переход между уровнями разделов"
                ),

                "expected": (
                    ".".join(
                        map(
                            str,
                            previous + [1]
                        )
                    )
                )
            }

        return None