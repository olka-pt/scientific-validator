# backend/app/rules/content/table_rule.py

import re

from backend.app.models.document import DocumentModel
from backend.app.models.validation import ValidationError
from backend.app.rules.base_rule import BaseRule


class TableRule(BaseRule):

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

        table_numbers = self._find_table_numbers(
            document
        )

        referenced_numbers = self._find_referenced_numbers(
            document
        )

        errors.extend(
            self._check_links_to_missing_tables(
                referenced_numbers=referenced_numbers,
                table_numbers=table_numbers,
            )
        )

        errors.extend(
            self._check_tables_without_links(
                table_numbers=table_numbers,
                referenced_numbers=referenced_numbers,
            )
        )

        errors.extend(
            self._check_sequential_numbering(
                table_numbers=table_numbers,
            )
        )

        return errors

    def _find_table_numbers(
        self,
        document: DocumentModel,
    ) -> set[int]:

        table_numbers = set()

        for paragraph in document.paragraphs:

            if paragraph.semantic_type != "table_caption":
                continue

            match = re.search(
                r"таблица\s*(\d+)",
                paragraph.text,
                re.IGNORECASE,
            )

            if match:
                table_numbers.add(
                    int(match.group(1))
                )

        return table_numbers

    def _find_referenced_numbers(
        self,
        document: DocumentModel,
    ) -> set[int]:

        referenced_numbers = set()

        for paragraph in document.paragraphs:

            if paragraph.semantic_type == "table_caption":
                continue

            matches = re.findall(
                r"(?:табл\.?|таблица|таблице|таблицы)\s*(\d+)",
                paragraph.text,
                re.IGNORECASE,
            )

            for match in matches:
                referenced_numbers.add(
                    int(match)
                )

        return referenced_numbers

    def _check_links_to_missing_tables(
        self,
        referenced_numbers: set[int],
        table_numbers: set[int],
    ) -> list[ValidationError]:

        errors = []

        for table_number in sorted(referenced_numbers):

            if table_number in table_numbers:
                continue

            errors.append(
                ValidationError(
                    category="tables",
                    message="Указана ссылка на несуществующую таблицу",
                    expected="Существующий номер таблицы",
                    actual=str(table_number),
                    paragraph_index=-1,
                    severity=self.reference_severity,
                )
            )

        return errors

    def _check_tables_without_links(
        self,
        table_numbers: set[int],
        referenced_numbers: set[int],
    ) -> list[ValidationError]:

        errors = []

        for table_number in sorted(table_numbers):

            if table_number in referenced_numbers:
                continue

            errors.append(
                ValidationError(
                    category="tables",
                    message="На таблицу нет ссылки в тексте",
                    expected=f"Ссылка на таблицу {table_number}",
                    actual="Ссылка отсутствует",
                    paragraph_index=-1,
                    severity=self.reference_severity,
                )
            )

        return errors

    def _check_sequential_numbering(
        self,
        table_numbers: set[int],
    ) -> list[ValidationError]:

        errors = []

        if not table_numbers:
            return errors

        sorted_numbers = sorted(
            table_numbers
        )

        expected_numbers = set(
            range(
                1,
                max(sorted_numbers) + 1,
            )
        )

        missing_numbers = sorted(
            expected_numbers - table_numbers
        )

        for missing_number in missing_numbers:

            errors.append(
                ValidationError(
                    category="tables",
                    message="Нарушена последовательная нумерация таблиц",
                    expected=f"Таблица {missing_number}",
                    actual="Номер пропущен",
                    paragraph_index=-1,
                    severity=self.numbering_severity,
                )
            )

        return errors