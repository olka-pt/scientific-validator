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


class DuplicateReferenceRule(BaseRule):

    def check(
        self,
        document: DocumentModel
    ) -> list[ValidationError]:

        errors = []

        seen_references = {}

        for paragraph in (
            document.paragraphs
        ):

            if (
                paragraph.semantic_type
                != "reference_item"
            ):
                continue

            normalized_text = re.sub(
                r"^\d+\.\s*",
                "",
                paragraph.text
            )

            normalized_text = (
                normalized_text
                .strip()
                .lower()
            )

            if (
                normalized_text
                in seen_references
            ):

                errors.append(
                    ValidationError(
                        category="references",

                        message=(
                            "Обнаружен дублирующийся источник"
                        ),

                        expected="Уникальный источник",

                        actual=paragraph.text,

                        paragraph_index=(
                            paragraph.paragraph_index
                        )
                    )
                )

            else:

                seen_references[
                    normalized_text
                ] = (
                    paragraph.paragraph_index
                )

        return errors