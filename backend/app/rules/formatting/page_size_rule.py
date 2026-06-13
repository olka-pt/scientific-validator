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


class PageSizeRule(BaseRule):

    def __init__(
        self,
        expected_width: float,
        expected_height: float,
        tolerance: float = 1.0
    ):

        self.expected_width = (
            expected_width
        )

        self.expected_height = (
            expected_height
        )

        self.tolerance = tolerance

    def check(
        self,
        document: DocumentModel
    ) -> list[ValidationError]:

        errors = []

        actual_width = (
            document.page_size.width
        )

        actual_height = (
            document.page_size.height
        )

        width_valid = (
            is_within_tolerance(
                actual=actual_width,
                expected=self.expected_width,
                tolerance=self.tolerance
            )
        )

        height_valid = (
            is_within_tolerance(
                actual=actual_height,
                expected=self.expected_height,
                tolerance=self.tolerance
            )
        )

        if not width_valid:

            errors.append(
                ValidationError(
                    category="formatting",

                    message=(
                        "Invalid page width"
                    ),

                    expected=str(
                        self.expected_width
                    ),

                    actual=str(
                        actual_width
                    ),

                    paragraph_index=-1
                )
            )

        if not height_valid:

            errors.append(
                ValidationError(
                    category="formatting",

                    message=(
                        "Invalid page height"
                    ),

                    expected=str(
                        self.expected_height
                    ),

                    actual=str(
                        actual_height
                    ),

                    paragraph_index=-1
                )
            )

        return errors