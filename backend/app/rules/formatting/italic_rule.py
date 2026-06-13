from backend.app.rules.formatting.base_formatting_rule import (
    BaseFormattingRule
)


class ItalicRule(
    BaseFormattingRule
):

    field_name = "italic"

    error_message = (
        "Invalid italic formatting"
    )