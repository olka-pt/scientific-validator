# backend/app/rules/content/foreign_reference_rule.py

import re

from backend.app.config.semantic_types import REFERENCE_ITEM
from backend.app.models.document import DocumentModel
from backend.app.models.validation import ValidationError
from backend.app.rules.base_rule import BaseRule


class ForeignReferenceRule(BaseRule):

    LATIN_PATTERN = re.compile(
        r"[A-Za-z]"
    )

    CYRILLIC_PATTERN = re.compile(
        r"[А-Яа-яЁё]"
    )

    def __init__(
        self,
        min_foreign_references: int = 2,
        severity: str = "critical",
    ):
        self.min_foreign_references = min_foreign_references
        self.severity = severity

    def check(
        self,
        document: DocumentModel,
    ) -> list[ValidationError]:

        references = [
            paragraph.text.strip()
            for paragraph in document.paragraphs
            if paragraph.semantic_type == REFERENCE_ITEM
            and paragraph.text.strip()
        ]

        foreign_references = [
            reference
            for reference in references
            if self._is_foreign_reference(reference)
        ]

        if len(foreign_references) >= self.min_foreign_references:
            return []

        return [
            ValidationError(
                category="references",
                message="Недостаточно иностранных источников",
                expected=f"Не менее {self.min_foreign_references} иностранных источников",
                actual=f"Найдено: {len(foreign_references)}",
                paragraph_index=-1,
                severity=self.severity,
            )
        ]

    def _is_foreign_reference(
        self,
        reference: str,
    ) -> bool:

        has_latin = bool(
            self.LATIN_PATTERN.search(reference)
        )

        has_cyrillic = bool(
            self.CYRILLIC_PATTERN.search(reference)
        )

        return has_latin and not has_cyrillic