# backend/app/rules/content/figure_rule.py

import re

from backend.app.models.document import DocumentModel
from backend.app.models.validation import ValidationError
from backend.app.rules.base_rule import BaseRule


class FigureRule(BaseRule):

    def __init__(
        self,
        reference_severity: str = "warning",
        numbering_severity: str = "critical",
    ):
        self.reference_severity = reference_severity
        self.numbering_severity = numbering_severity

    def check(
        self,
        document: DocumentModel,
    ) -> list[ValidationError]:

        errors = []

        figure_numbers = self._find_figure_numbers(
            document
        )

        referenced_numbers = self._find_referenced_numbers(
            document
        )

        errors.extend(
            self._check_links_to_missing_figures(
                referenced_numbers=referenced_numbers,
                figure_numbers=figure_numbers,
            )
        )

        errors.extend(
            self._check_figures_without_links(
                figure_numbers=figure_numbers,
                referenced_numbers=referenced_numbers,
            )
        )

        errors.extend(
            self._check_sequential_numbering(
                figure_numbers=figure_numbers,
            )
        )

        return errors

    def _find_figure_numbers(
        self,
        document: DocumentModel,
    ) -> set[int]:

        figure_numbers = set()

        for paragraph in document.paragraphs:

            if paragraph.semantic_type != "caption":
                continue

            match = re.search(
                r"(?:рис\.?|рисунок)\s*(\d+)",
                paragraph.text,
                re.IGNORECASE,
            )

            if match:
                figure_numbers.add(
                    int(match.group(1))
                )

        return figure_numbers

    def _find_referenced_numbers(
        self,
        document: DocumentModel,
    ) -> set[int]:

        referenced_numbers = set()

        for paragraph in document.paragraphs:

            if paragraph.semantic_type == "caption":
                continue

            matches = re.findall(
                r"(?:рис\.?|рисунок|рисунке|рисунка)\s*(\d+)",
                paragraph.text,
                re.IGNORECASE,
            )

            for match in matches:
                referenced_numbers.add(
                    int(match)
                )

        return referenced_numbers

    def _check_links_to_missing_figures(
        self,
        referenced_numbers: set[int],
        figure_numbers: set[int],
    ) -> list[ValidationError]:

        errors = []

        for figure_number in sorted(referenced_numbers):

            if figure_number in figure_numbers:
                continue

            errors.append(
                ValidationError(
                    category="figures",
                    message="Указана ссылка на несуществующий рисунок",
                    expected="Существующий номер рисунка",
                    actual=str(figure_number),
                    paragraph_index=-1,
                    severity=self.reference_severity,
                )
            )

        return errors

    def _check_figures_without_links(
        self,
        figure_numbers: set[int],
        referenced_numbers: set[int],
    ) -> list[ValidationError]:

        errors = []

        for figure_number in sorted(figure_numbers):

            if figure_number in referenced_numbers:
                continue

            errors.append(
                ValidationError(
                    category="figures",
                    message="На рисунок нет ссылки в тексте",
                    expected=f"Ссылка на рисунок {figure_number}",
                    actual="Ссылка отсутствует",
                    paragraph_index=-1,
                    severity=self.reference_severity,
                )
            )

        return errors

    def _check_sequential_numbering(
        self,
        figure_numbers: set[int],
    ) -> list[ValidationError]:

        errors = []

        if not figure_numbers:
            return errors

        sorted_numbers = sorted(
            figure_numbers
        )

        expected_numbers = set(
            range(
                1,
                max(sorted_numbers) + 1,
            )
        )

        missing_numbers = sorted(
            expected_numbers - figure_numbers
        )

        for missing_number in missing_numbers:

            errors.append(
                ValidationError(
                    category="figures",
                    message="Нарушена последовательная нумерация рисунков",
                    expected=f"Рисунок {missing_number}",
                    actual="Номер пропущен",
                    paragraph_index=-1,
                    severity=self.numbering_severity,
                )
            )

        return errors