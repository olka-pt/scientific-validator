from backend.app.models.document import (
    DocumentModel
)

from backend.app.models.validation import (
    ValidationError
)

from backend.app.rules.base_rule import (
    BaseRule
)


class AbstractLengthRule(BaseRule):

    def __init__(
        self,
        min_words: int = 100,
        max_words: int = 300
    ):

        self.min_words = (
            min_words
        )

        self.max_words = (
            max_words
        )

    def check(
        self,
        document: DocumentModel
    ) -> list[ValidationError]:

        errors = []

        for paragraph in (
            document.paragraphs
        ):

            if (
                paragraph.semantic_type
                not in [
                    "abstract_ru",
                    "abstract_en"
                ]
            ):
                continue

            text = paragraph.text

            words = text.split()

            word_count = len(
                words
            )

            if (
                word_count
                < self.min_words
            ):

                errors.append(
                    ValidationError(
                        category="abstract",

                        message=(
                            "Аннотация слишком короткая"
                        ),

                        expected=str(
                            self.min_words
                        ),

                        actual=str(
                            word_count
                        ),

                        paragraph_index=(
                            paragraph.paragraph_index
                        )
                    )
                )

            if (
                word_count
                > self.max_words
            ):

                errors.append(
                    ValidationError(
                        category="abstract",

                        message=(
                            "Аннотация слишком длинная"
                        ),

                        expected=str(
                            self.max_words
                        ),

                        actual=str(
                            word_count
                        ),

                        paragraph_index=(
                            paragraph.paragraph_index
                        )
                    )
                )

        return errors