from backend.app.rules.formatting.base_formatting_rule import (
    BaseFormattingRule
)


class AlignmentRule(
    BaseFormattingRule
):

    field_name = "alignment"

    error_message = (
        "Invalid alignment"
    )