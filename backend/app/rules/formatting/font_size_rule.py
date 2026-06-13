# backend/app/rules/formatting/font_size_rule.py

from backend.app.rules.formatting.base_formatting_rule import (
    BaseFormattingRule
)


class FontSizeRule(BaseFormattingRule):

    field_name = "font_size"

    error_message = "Invalid font size"

    tolerance = 0.5