from backend.app.rules.formatting.base_formatting_rule import (
    BaseFormattingRule
)


class SpaceBeforeRule(
    BaseFormattingRule
):

    field_name = "space_before"

    error_message = (
        "Invalid space before"
    )

    tolerance = 0.2