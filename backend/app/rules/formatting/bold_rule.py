from backend.app.rules.formatting.base_formatting_rule import (
    BaseFormattingRule
)


class BoldRule(
    BaseFormattingRule
):

    field_name = "bold"

    error_message = (
        "Invalid bold formatting"
    )