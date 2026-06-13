from backend.app.models.document import (
    DocumentModel
)

from backend.app.models.validation import (
    ValidationError
)

from backend.app.rules.base_rule import (
    BaseRule
)

from backend.app.utils.tolerance import (
    is_within_tolerance
)


class BaseFormattingRule(BaseRule):

    field_name: str = ""

    error_message: str = ""

    tolerance: float = 0.0

    def __init__(
        self,
        expected_values: dict[str, float | str | bool]
    ):

        self.expected_values = (
            expected_values
        )

    def check(
        self,
        document: DocumentModel
    ) -> list[ValidationError]:

        errors = []

        for paragraph in (
            document.paragraphs
        ):

            semantic_type = (
                paragraph.semantic_type
            )

            expected_value = (
                self.expected_values.get(
                    semantic_type
                )
            )

            if expected_value is None:
                continue

            actual_value = getattr(
                paragraph,
                self.field_name
            )

            if actual_value is None:

                if expected_value == 0:

                    actual_value = 0
                
                else:

                    errors.append(
                        ValidationError(
                            category="formatting",

                            message=self.error_message,

                            expected=str(
                                expected_value
                            ),

                            actual="None",

                            paragraph_index=(
                                paragraph.paragraph_index
                            )
                        )
                    )

                    continue
                
            if isinstance(
                expected_value,
                (int, float)
            ):

                is_valid = (
                    is_within_tolerance(
                        actual=actual_value,
                        expected=expected_value,
                        tolerance=self.tolerance
                    )
                )

            else:

                is_valid = (
                    actual_value
                    == expected_value
                )

            if not is_valid:

                errors.append(
                    ValidationError(
                        category="formatting",

                        message=(
                            self.error_message
                        ),

                        expected=str(
                            expected_value
                        ),

                        actual=str(
                            actual_value
                        ),

                        paragraph_index=(
                            paragraph.paragraph_index
                        )
                    )
                )

        return errors