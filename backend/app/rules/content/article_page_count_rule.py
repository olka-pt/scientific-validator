# backend/app/rules/content/article_page_count_rule.py

from backend.app.models.document import DocumentModel
from backend.app.models.validation import ValidationError
from backend.app.rules.base_rule import BaseRule


class ArticlePageCountRule(BaseRule):

    def __init__(
        self,
        min_pages: int,
        max_pages: int,
        severity: str = "warning",
    ):
        self.min_pages = min_pages
        self.max_pages = max_pages
        self.severity = severity

    def check(
        self,
        document: DocumentModel,
    ) -> list[ValidationError]:

        if document.page_count is None:
            return [
                ValidationError(
                    category="structure",
                    message="Не удалось определить количество страниц документа",
                    expected=f"От {self.min_pages} до {self.max_pages} страниц",
                    actual="Количество страниц не определено",
                    paragraph_index=-1,
                    severity=self.severity,
                )
            ]

        if (
            self.min_pages
            <= document.page_count
            <= self.max_pages
        ):
            return []

        return [
            ValidationError(
                category="structure",
                message="Неверный объем статьи",
                expected=f"От {self.min_pages} до {self.max_pages} страниц",
                actual=f"{document.page_count} страниц",
                paragraph_index=-1,
                severity=self.severity,
            )
        ]