import re

from backend.app.models.document import (
    DocumentModel
)

from backend.app.models.validation import (
    ValidationError
)

from backend.app.rules.base_rule import (
    BaseRule
)


class SequentialNumberingRule(BaseRule):

    def check(
        self,
        document: DocumentModel
    ) -> list[ValidationError]:

        errors = []

        reference_numbers = []

        for paragraph in (
            document.paragraphs
        ):

            if (
                paragraph.semantic_type
                == "reference_item"
            ):

                match = re.match(
                    r"^(\d+)\.",
                    paragraph.text.strip()
                )

                if match:

                    reference_numbers.append(
                        int(match.group(1))
                    )

        expected = 1

        for actual in reference_numbers:

            if actual != expected:

                errors.append(
                    ValidationError(
                        category="numbering",

                        message=(
                            "Нарушена последовательность нумерации источников"
                        ),

                        expected=str(expected),

                        actual=str(actual),

                        paragraph_index=actual
                    )
                )

            expected += 1

        return errors