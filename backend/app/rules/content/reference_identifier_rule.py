# backend/app/rules/content/reference_identifier_rule.py

import re

from backend.app.config.semantic_types import REFERENCE_ITEM
from backend.app.models.document import DocumentModel
from backend.app.models.validation import ValidationError
from backend.app.rules.base_rule import BaseRule


class ReferenceIdentifierRule(BaseRule):

    DOI_PATTERN = re.compile(
        r"\bdoi\s*:?\s*10\.\d{4,9}/[-._;()/:a-zA-Z0-9]+",
        re.IGNORECASE,
    )

    EDN_PATTERN = re.compile(
        r"\bedn\s+[a-zA-Z0-9]{4,}",
        re.IGNORECASE,
    )

    URL_PATTERN = re.compile(
        r"\b(?:https?://|www\.)\S+",
        re.IGNORECASE,
    )

    ISBN_PATTERN = re.compile(
        r"\bisbn\s*(?:97[89][-\s]?)?[\d\-\s]{9,17}[\dXx]",
        re.IGNORECASE,
    )

    REFERENCE_START_PATTERN = re.compile(
        r"^\s*\d+\s*[\.\)]"
    )

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

        references = self._collect_reference_blocks(
            document
        )

        for index, reference_text in enumerate(
            references,
            start=1,
        ):
            if self._has_identifier(reference_text):
                continue

            errors.append(
                ValidationError(
                    category="references",
                    message="В источнике отсутствует DOI, EDN, URL или ISBN",
                    expected="DOI, EDN, URL или ISBN",
                    actual=reference_text[:180],
                    paragraph_index=-1,
                    severity=self.severity,
                )
            )

        return errors

    def _collect_reference_blocks(
        self,
        document: DocumentModel,
    ) -> list[str]:

        reference_paragraphs = [
            paragraph.text.strip()
            for paragraph in document.paragraphs
            if paragraph.semantic_type == REFERENCE_ITEM
            and paragraph.text.strip()
        ]

        if not reference_paragraphs:
            return []

        blocks = []
        current_block = []

        for text in reference_paragraphs:

            if self.REFERENCE_START_PATTERN.match(text):

                if current_block:
                    blocks.append(
                        " ".join(current_block)
                    )

                current_block = [text]

            else:

                if current_block:
                    current_block.append(text)
                else:
                    current_block = [text]

        if current_block:
            blocks.append(
                " ".join(current_block)
            )

        return blocks

    def _has_identifier(
        self,
        text: str,
    ) -> bool:

        return any(
            pattern.search(text)
            for pattern in (
                self.DOI_PATTERN,
                self.EDN_PATTERN,
                self.URL_PATTERN,
                self.ISBN_PATTERN,
            )
        )