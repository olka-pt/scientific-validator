from backend.app.models.document import DocumentModel
from backend.app.models.validation import ValidationError
from backend.app.rules.base_rule import BaseRule


class VkrChapterNewPageRule(BaseRule):

    REQUIRED_NEW_PAGE_SECTIONS = {
        "introduction",
        "analytical_section",
        "special_section",
        "economic_efficiency_section",
        "conclusion",
        "references",
    }

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

        for paragraph in document.paragraphs:

            if paragraph.semantic_type not in self.REQUIRED_NEW_PAGE_SECTIONS:
                continue

            if paragraph.starts_new_page:
                continue

            errors.append(
                ValidationError(
                    category="structure",
                    message="Новая глава должна начинаться с новой страницы",
                    expected="Разрыв страницы перед главой",
                    actual=paragraph.text,
                    paragraph_index=paragraph.paragraph_index,
                    severity=self.severity,
                )
            )

        return errors