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


class LanguageConsistencyRule(BaseRule):

    LANGUAGE_PAIRS = {
        "title_ru": "title_en",

        "abstract_ru": "abstract_en",

        "keywords_ru": "keywords_en"
    }

    CYRILLIC_PATTERN = (
        r"[а-яА-Я]"
    )

    LATIN_PATTERN = (
        r"[a-zA-Z]"
    )

    RUSSIAN_SECTIONS = [
        "title_ru",
        "abstract_ru",
        "keywords_ru"
    ]

    ENGLISH_SECTIONS = [
        "title_en",
        "abstract_en",
        "keywords_en"
    ]

    def check(
        self,
        document: DocumentModel
    ) -> list[ValidationError]:

        errors = []

        semantic_types = {
            paragraph.semantic_type
            for paragraph in (
                document.paragraphs
            )
        }

        # RU/EN pair consistency

        for (
            ru_section,
            en_section
        ) in (
            self.LANGUAGE_PAIRS.items()
        ):

            if (
                ru_section
                in semantic_types

                and

                en_section
                not in semantic_types
            ):

                errors.append(
                    ValidationError(
                        category="language",

                        message=(
                            "Отсутствует английская версия раздела"
                        ),

                        expected=f"Раздел {en_section}",

                        actual="Отсутствует",

                        paragraph_index=-1
                    )
                )

            if (
                en_section
                in semantic_types

                and

                ru_section
                not in semantic_types
            ):

                errors.append(
                    ValidationError(
                        category="language",

                        message=(
                            "Отсутствует русская версия раздела"
                        ),

                        expected=f"Раздел {ru_section}",

                        actual="Отсутствует",

                        paragraph_index=-1
                    )
                )

        # Language detection

        for paragraph in (
            document.paragraphs
        ):

            semantic_type = (
                paragraph.semantic_type
            )

            text = (
                paragraph.text
            )

            # Russian sections

            if (
                semantic_type
                in self.RUSSIAN_SECTIONS
            ):

                has_cyrillic = re.search(
                    self.CYRILLIC_PATTERN,
                    text
                )

                if not has_cyrillic:

                    errors.append(
                        ValidationError(
                            category="language",

                            message=(
                                "Русский раздел не содержит кириллицу"
                            ),

                            expected="Кириллица",

                            actual=text[:50],

                            paragraph_index=(
                                paragraph.paragraph_index
                            )
                        )
                    )

            # English sections

            if (
                semantic_type
                in self.ENGLISH_SECTIONS
            ):

                has_latin = re.search(
                    self.LATIN_PATTERN,
                    text
                )

                if not has_latin:

                    errors.append(
                        ValidationError(
                            category="language",

                            message=(
                                "Английский раздел не содержит латиницу"
                            ),

                            expected="Латиница",

                            actual=text[:50],

                            paragraph_index=(
                                paragraph.paragraph_index
                            )
                        )
                    )

        return errors