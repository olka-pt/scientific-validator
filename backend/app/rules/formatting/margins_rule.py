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


class MarginsRule(BaseRule):

    def __init__(
        self,
        expected_margins: dict[str, float],
        tolerance: float = 0.1
    ):

        self.expected_margins = (
            expected_margins
        )

        self.tolerance = tolerance

    def check(
        self,
        document: DocumentModel
    ) -> list[ValidationError]:

        errors = []

        actual_margins = (
            document.margins
        )

        for margin_name, expected_value in (
            self.expected_margins.items()
        ):

            actual_value = (
                getattr(
                actual_margins,
                    margin_name
                )
            )

            if actual_value is None:

                errors.append(
                    ValidationError(
                        category="formatting",

                        message=(
                            f"Missing {margin_name} margin"
                        ),

                        expected=str(
                            expected_value
                        ),

                        actual="None",

                        paragraph_index=-1
                    )
                )

                continue

            is_valid = (
                is_within_tolerance(
                    actual=actual_value,
                    expected=expected_value,
                    tolerance=self.tolerance
                )
            )

            if not is_valid:

                errors.append(
                    ValidationError(
                        category="formatting",

                        message=(
                            f"Invalid {margin_name} margin"
                        ),

                        expected=str(
                            expected_value
                        ),

                        actual=str(
                            actual_value
                        ),

                        paragraph_index=-1
                    )
                )

        return errors