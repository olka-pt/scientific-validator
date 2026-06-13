from backend.app.models.document import (
    DocumentModel
)

from backend.app.models.validation import (
    ValidationError
)

from backend.app.rules.base_rule import (
    BaseRule
)


class KeywordCountRule(BaseRule):

    def __init__(
        self,
        min_keywords: int = 5,
        max_keywords: int = 10
    ):

        self.min_keywords = (
            min_keywords
        )

        self.max_keywords = (
            max_keywords
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
                    "keywords_ru",
                    "keywords_en"
                ]
            ):
                continue

            text = paragraph.text

            text = text.replace(
                "Ключевые слова:",
                ""
            )

            text = text.replace(
                "Keywords:",
                ""
            )

            keywords = [
                keyword.strip()
                for keyword in (
                    text.split(",")
                )
                if keyword.strip()
            ]

            keyword_count = len(
                keywords
            )

            if (
                keyword_count
                < self.min_keywords
            ):

                errors.append(
                    ValidationError(
                        category="keywords",

                        message=(
                            "Недостаточное количество ключевых слов"
                        ),

                        expected=str(
                            f"Не менее {self.min_keywords}"
                        ),

                        actual=str(
                            keyword_count
                        ),

                        paragraph_index=(
                            paragraph.paragraph_index
                        )
                    )
                )

            if (
                keyword_count
                > self.max_keywords
            ):

                errors.append(
                    ValidationError(
                        category="keywords",

                        message=(
                            "Слишком большое количество ключевых слов"
                        ),

                        expected=str(
                            f"Не более {self.max_keywords}"
                        ),

                        actual=str(
                            keyword_count
                        ),

                        paragraph_index=(
                            paragraph.paragraph_index
                        )
                    )
                )

        return errors