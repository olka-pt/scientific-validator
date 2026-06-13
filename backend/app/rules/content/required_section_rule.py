# backend/app/rules/content/required_section_rule.py

from backend.app.models.document import (
    DocumentModel
)

from backend.app.models.validation import (
    ValidationError
)

from backend.app.rules.base_rule import (
    BaseRule
)


class RequiredSectionRule(BaseRule):

    def __init__(
        self,
        required_sections: list[str],
        severity: str = "critical",
    ):
        self.required_sections = required_sections
        self.severity = severity

    def check(
        self,
        document: DocumentModel
    ) -> list[ValidationError]:

        errors = []

        semantic_types = {
            paragraph.semantic_type
            for paragraph in document.paragraphs
        }

        for required_section in self.required_sections:

            if required_section not in semantic_types:

                errors.append(
                    ValidationError(
                        category="structure",
                        message="Отсутствует обязательный раздел",
                        expected=required_section,
                        actual="Отсутствует",
                        paragraph_index=-1,
                        severity=self.severity,
                    )
                )

        return errors