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


class AffiliationRule(BaseRule):

    ORGANIZATION_KEYWORDS = [

        # RU

        "университет",
        "институт",
        "академия",
        "федеральный",
        "научный",
        "кафедра",
        "факультет",

        # EN

        "university",
        "institute",
        "academy",
        "research",
        "faculty",
        "department",
        "school"
    ]

    UNIVERSITY_DICTIONARY = [

        # RU abbreviations

        "кфу",
        "кгэу",
        "kspeu",
        "книту",
        "книту-каи",
        "мгу",
        "спбгу",
        "вшэ",

        # RU full names

        "казанский федеральный университет",

        (
            "казанский государственный "
            "энергетический университет"
        ),

        (
            "казанский национальный "
            "исследовательский технический "
            "университет"
        ),

        "московский государственный университет",

        # EN universities

        "mit",
        "stanford",
        "harvard",
        "oxford",
        "cambridge"
    ]

    ABBREVIATION_PATTERN = (
        r"^[A-ZА-ЯЁ0-9\-]{2,}$"
    )

    MIN_LENGTH = 3

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
                != "affiliation"
            ):
                continue

            text = (
                paragraph.text.strip()
            )

            if not text:

                errors.append(
                    ValidationError(
                        category="affiliation",

                        message=(
                            "Название организации отсутствует"
                        ),

                        expected=(
                            "Название организации"
                        ),

                        actual="Пусто",

                        paragraph_index=(
                            paragraph.paragraph_index
                        )
                    )
                )

                continue

            if (
                len(text)
                < self.MIN_LENGTH
            ):

                errors.append(
                    ValidationError(
                        category="affiliation",

                        message=(
                            "Название организации слишком короткое"
                        ),

                        expected=(
                            f">= {self.MIN_LENGTH} символов"
                        ),

                        actual=str(
                            len(text)
                        ),

                        paragraph_index=(
                            paragraph.paragraph_index
                        )
                    )
                )

                continue

            lower_text = (
                text.lower()
            )

            has_keyword = any(
                keyword in lower_text
                for keyword in (
                    self.ORGANIZATION_KEYWORDS
                )
            )

            abbreviations = re.findall(
                r"\b[A-ZА-ЯЁ\-]{2,}\b",
                text
            )

            has_abbreviation = bool(
                abbreviations
            )

            has_dictionary_match = any(
                university in lower_text
                for university in (
                    self.UNIVERSITY_DICTIONARY
                )
            )

            if (
                not has_keyword
                and
                not has_abbreviation
                and
                not has_dictionary_match
            ):

                errors.append(
                    ValidationError(
                        category="affiliation",

                        message=(
                            "Название организации не похоже на учебное или научное учреждение"
                        ),

                        expected=(
                            "Название университета, института или общепринятое сокращение"
                        ),

                        actual=text[:50],

                        paragraph_index=(
                            paragraph.paragraph_index
                        )
                    )
                )

        return errors