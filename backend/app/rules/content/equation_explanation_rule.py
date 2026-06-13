# backend/app/rules/content/equation_explanation_rule.py

import re

from backend.app.models.document import DocumentModel
from backend.app.models.validation import ValidationError
from backend.app.rules.base_rule import BaseRule


class EquationExplanationRule(BaseRule):

    def __init__(
        self,
        severity: str = "warning",
        max_paragraphs_after: int = 3,
    ):
        self.severity = severity
        self.max_paragraphs_after = max_paragraphs_after

    def check(
        self,
        document: DocumentModel,
    ) -> list[ValidationError]:

        errors = []

        for index, paragraph in enumerate(document.paragraphs):

            if paragraph.semantic_type != "equation":
                continue

            if self._has_explanation_after(
                document=document,
                equation_index=index,
            ):
                continue

            errors.append(
                ValidationError(
                    category="equations",
                    message="После формулы отсутствует пояснение обозначений",
                    expected="Пояснение после формулы, например: где x — ...",
                    actual="Пояснение не найдено",
                    paragraph_index=paragraph.paragraph_index,
                    severity=self.severity,
                )
            )

        return errors

    def _has_explanation_after(
        self,
        document: DocumentModel,
        equation_index: int,
    ) -> bool:

        start_index = equation_index + 1

        end_index = min(
            len(document.paragraphs),
            equation_index + 1 + self.max_paragraphs_after,
        )

        for paragraph in document.paragraphs[start_index:end_index]:

            text = paragraph.text.strip().lower()

            if not text:
                continue

            if self._looks_like_new_section(paragraph):
                return False

            if self._looks_like_explanation(text):
                return True

        return False

    @staticmethod
    def _looks_like_explanation(
        text: str,
    ) -> bool:

        explanation_patterns = (
            r"^где\b",
            r"^здесь\b",
            r"^where\b",
            r"^[a-zа-яё]\s*[—-]\s*",
            r"^[a-zа-яё]\s*,\s*[a-zа-яё]\s*[—-]\s*",
        )

        return any(
            re.search(pattern, text, re.IGNORECASE)
            for pattern in explanation_patterns
        )

    @staticmethod
    def _looks_like_new_section(
        paragraph,
    ) -> bool:

        return (
            paragraph.bold
            and paragraph.alignment == "center"
            and len(paragraph.text.strip()) < 120
        )