# backend/app/rules/content/author_count_rule.py

import re

from backend.app.config.semantic_types import AUTHORS
from backend.app.models.document import DocumentModel
from backend.app.models.validation import ValidationError
from backend.app.rules.base_rule import BaseRule


class AuthorCountRule(BaseRule):

    CYRILLIC_PATTERN = re.compile(
        r"[а-яА-Я]"
    )

    AUTHOR_PATTERN = re.compile(
        r"[А-ЯЁA-Z][а-яёa-z\-]+"
        r"\s+"
        r"[А-ЯЁA-Z]\."
        r"\s*"
        r"[А-ЯЁA-Z]\."
    )

    def __init__(
        self,
        max_authors: int = 3,
        severity: str = "warning",
    ):
        self.max_authors = max_authors
        self.severity = severity

    def check(
        self,
        document: DocumentModel,
    ) -> list[ValidationError]:

        authors = []

        for paragraph in document.paragraphs:

            if paragraph.semantic_type != AUTHORS:
                continue

            if not self.CYRILLIC_PATTERN.search(
                paragraph.text
            ):
                continue

            found_authors = re.findall(
                self.AUTHOR_PATTERN,
                paragraph.text,
            )

            authors.extend(
                author.strip()
                for author in found_authors
                if author.strip()
            )

        unique_authors = list(
            dict.fromkeys(authors)
        )

        if len(unique_authors) <= self.max_authors:
            return []

        return [
            ValidationError(
                category="authors",
                message="Превышено допустимое количество авторов",
                expected=f"Не более {self.max_authors} авторов",
                actual=f"Авторов: {len(unique_authors)}",
                paragraph_index=-1,
                severity=self.severity,
            )
        ]