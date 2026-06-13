from backend.app.rules.formatting.base_formatting_rule import (
    BaseFormattingRule
)


class SpaceAfterRule(
    BaseFormattingRule
):

    field_name = "space_after"

    error_message = (
        "Invalid space after"
    )

    tolerance = 0.2