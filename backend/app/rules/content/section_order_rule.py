# backend/app/rules/content/section_order_rule.py

from backend.app.models.document import DocumentModel
from backend.app.models.validation import ValidationError
from backend.app.rules.base_rule import BaseRule


class SectionOrderRule(BaseRule):

    def __init__(
        self,
        section_groups: list[set[str]],
        severity: str = "critical",
    ):
        self.section_groups = section_groups
        self.severity = severity

    def check(
        self,
        document: DocumentModel,
    ) -> list[ValidationError]:

        errors = []
        found_sections = []

        for paragraph in document.paragraphs:
            semantic_type = paragraph.semantic_type

            is_known_section = any(
                semantic_type in group
                for group in self.section_groups
            )

            if (
                is_known_section
                and semantic_type not in found_sections
            ):
                found_sections.append(semantic_type)

        previous_index = -1

        for section in found_sections:
            current_index = None

            for index, group in enumerate(self.section_groups):
                if section in group:
                    current_index = index
                    break

            if current_index is None:
                continue

            if current_index < previous_index:
                errors.append(
                    ValidationError(
                        category="structure",
                        message="Нарушен порядок разделов документа",
                        expected="Корректная последовательность разделов",
                        actual=section,
                        paragraph_index=-1,
                        severity=self.severity,
                    )
                )

            previous_index = current_index

        return errors