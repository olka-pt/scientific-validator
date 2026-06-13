# backend/app/rules/formatting/first_line_indent_rule.py

from backend.app.models.document import DocumentModel
from backend.app.models.validation import ValidationError
from backend.app.rules.formatting.base_formatting_rule import BaseFormattingRule
from backend.app.utils.tolerance import is_within_tolerance


class FirstLineIndentRule(BaseFormattingRule):

    field_name = "first_line_indent"

    error_message = "Invalid first line indent"

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

            actual_value = paragraph.first_line_indent

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