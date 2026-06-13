# backend/app/rules/content/equation_number_sequence_rule.py

import re

from backend.app.models.document import DocumentModel
from backend.app.models.validation import ValidationError
from backend.app.rules.base_rule import BaseRule


class EquationNumberSequenceRule(BaseRule):

    def __init__(
        self,
        severity: str = "critical",
    ):
        self.severity = severity

    def check(
        self,
        document: DocumentModel,
    ) -> list[ValidationError]:

        errors = []

        equation_numbers = self._find_equation_numbers(
            document
        )

        if not equation_numbers:
            return errors

        expected_numbers = set(
            range(
                1,
                max(equation_numbers) + 1,
            )
        )

        missing_numbers = sorted(
            expected_numbers - equation_numbers
        )

        for missing_number in missing_numbers:

            errors.append(
                ValidationError(
                    category="equations",
                    message="Нарушена последовательная нумерация формул",
                    expected=f"Формула ({missing_number})",
                    actual="Номер пропущен",
                    paragraph_index=-1,
                    severity=self.severity,
                )
            )

        return errors

    def _find_equation_numbers(
        self,
        document: DocumentModel,
    ) -> set[int]:

        equation_numbers = set()

        for paragraph in document.paragraphs:

            if paragraph.semantic_type != "equation":
                continue

            match = re.search(
                r"\((\d+)\)\s*$",
                paragraph.text.strip(),
            )

            if match:
                equation_numbers.add(
                    int(match.group(1))
                )

        return equation_numbers