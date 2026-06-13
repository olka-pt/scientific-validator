from backend.app.models.document import (
    DocumentModel
)

from backend.app.models.validation import (
    ValidationError
)

from backend.app.rules.base_rule import (
    BaseRule
)

from backend.app.config.semantic_types import (
    TITLE_RU,
    ABSTRACT_RU,
    KEYWORDS_RU,
    REFERENCES_HEADER,
    REFERENCE_ITEM,
)


class EmptySectionRule(BaseRule):

    REQUIRED_SECTIONS = [
        TITLE_RU,
        ABSTRACT_RU,
        KEYWORDS_RU,
        REFERENCES_HEADER
    ]

    SECTION_NAMES = {

        TITLE_RU:
        "Название",

        ABSTRACT_RU:
        "Аннотация",

        KEYWORDS_RU:
        "Ключевые слова",

        REFERENCES_HEADER:
        "Список литературы",
    }

    def check(
        self,
        document: DocumentModel
    ) -> list[ValidationError]:

        errors = []

        semantic_types = [
            paragraph.semantic_type
            for paragraph in (
                document.paragraphs
            )
        ]

        for section in (
            self.REQUIRED_SECTIONS
        ):

            if section not in semantic_types:

                errors.append(
                    ValidationError(
                        category="structure",

                        message=(
                            "Отсутствует обязательный раздел"
                        ),

                        expected=(
                            self.SECTION_NAMES.get(
                                section,
                                section
                            )
                        ),

                        actual="Не найден",

                        paragraph_index=-1
                    )
                )

        has_references_header = (
            REFERENCES_HEADER in semantic_types
        )

        has_reference_items = (
            REFERENCE_ITEM in semantic_types
        )

        if (
            has_references_header
            and not has_reference_items
        ):

            errors.append(
                ValidationError(
                    category="structure",

                    message=(
                        "Раздел со списком литературы пуст"
                    ),

                    expected="Хотя бы один источник",

                    actual="Источники отсутствуют",

                    paragraph_index=-1
                )
            )

        return errors