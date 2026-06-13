# backend/app/rules/content/page_numbering_rule.py

from backend.app.models.document import DocumentModel
from backend.app.models.validation import ValidationError
from backend.app.rules.base_rule import BaseRule


class PageNumberingRule(BaseRule):

    def __init__(
        self,
        severity: str = "critical",
    ):
        self.severity = severity

    def check(
        self,
        document: DocumentModel,
    ) -> list[ValidationError]:

        if document.has_page_numbering:
            return []

        return [
            ValidationError(
                category="structure",
                message="В документе не найдена нумерация страниц",
                expected="Номер страницы в нижнем колонтитуле",
                actual="Нумерация страниц не найдена",
                paragraph_index=-1,
                severity=self.severity,
            )
        ]