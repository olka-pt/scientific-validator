# backend/app/rules/formatting/line_spacing_rule.py

from backend.app.models.document import DocumentModel
from backend.app.models.validation import ValidationError
from backend.app.rules.formatting.base_formatting_rule import BaseFormattingRule
from backend.app.utils.tolerance import is_within_tolerance


class LineSpacingRule(BaseFormattingRule):

    field_name = "line_spacing"

    error_message = "Invalid line spacing"

    tolerance = 0.2

    def check(
        self,
        document: DocumentModel,
    ) -> list[ValidationError]:

        errors = []

        for paragraph in document.paragraphs:

            expected_value = self.expected_values.get(
                paragraph.semantic_type
            )

            if expected_value is None:
                continue

            actual_value = paragraph.line_spacing

            if actual_value is None:
                continue

            if not is_within_tolerance(
                actual=actual_value,
                expected=expected_value,
                tolerance=self.tolerance,
            ):

                errors.append(
                    ValidationError(
                        category="formatting",
                        message=self.error_message,
                        expected=str(expected_value),
                        actual=str(actual_value),
                        paragraph_index=paragraph.paragraph_index,
                    )
                )

        return errors