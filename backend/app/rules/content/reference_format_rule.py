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


class ReferenceFormatRule(BaseRule):

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
                != "reference_item"
            ):
                continue

            text = paragraph.text.strip()

            has_number = bool(
                re.match(
                    r"^\d+\.",
                    text
                )
            )

            has_year = bool(
                re.search(
                    r"(19|20)\d{2}",
                    text
                )
            )

            has_separator = (
                "//" in text
            )

            has_dash = (
                "–" in text
            )

            is_electronic_resource = (
                "[Электронный ресурс]"
                in text
            )

            doi_match = re.search(
                r"10\.\d{4,9}/[-._;()/:A-Z0-9]+",
                text,
                re.IGNORECASE
            )

            has_doi = (
                "DOI" in text
            )

            url_match = re.search(
                r"https?://[^\s]+",
                text
            )

            has_url = (
                "URL" in text
            )

            edn_match = re.search(
                r"EDN\s+[A-Z]{6}",
                text
            )

            has_edn = (
                "EDN" in text
            )

            if not has_number:

                errors.append(
                    ValidationError(
                        category="references",

                        message=(
                            "Источник должен начинаться с номера"
                        ),

                        expected="Номер источника",

                        actual=text,

                        paragraph_index=(
                            paragraph.paragraph_index
                        )
                    )
                )

            if not has_year:

                errors.append(
                    ValidationError(
                        category="references",

                        message=(
                            "Отсутствует год публикации"
                        ),

                        expected="Год публикации",

                        actual=text,

                        paragraph_index=(
                            paragraph.paragraph_index
                        )
                    )
                )

            if not has_separator:

                errors.append(
                    ValidationError(
                        category="references",

                        message=(
                            "Отсутствует разделитель //"
                        ),

                        expected="Разделитель //",

                        actual=text,

                        paragraph_index=(
                            paragraph.paragraph_index
                        )
                    )
                )

            if (
                not has_dash
                and not is_electronic_resource
            ):

                errors.append(
                    ValidationError(
                        category="references",

                        message=(
                            "Отсутствует разделитель —"
                        ),

                        expected="Разделитель –",

                        actual=text,

                        paragraph_index=(
                            paragraph.paragraph_index
                        )
                    )
                )
            
            if has_doi and not doi_match:

                errors.append(
                    ValidationError(
                        category="references",

                        message=(
                            "Некорректный формат DOI"
                        ),

                        expected="Корректный DOI",

                        actual=text,

                        paragraph_index=(
                            paragraph.paragraph_index
                        )
                    )
                )
            
            if has_url and not url_match:

                errors.append(
                    ValidationError(
                        category="references",

                        message=(
                            "Некорректный формат URL"
                        ),

                        expected="Корректный URL",

                        actual=text,

                        paragraph_index=(
                            paragraph.paragraph_index
                        )
                    )
                )

            if has_edn and not edn_match:

                errors.append(
                    ValidationError(
                        category="references",

                        message=(
                            "Некорректный формат EDN"
                        ),

                        expected="Формат EDN ABCDEF",

                        actual=text,

                        paragraph_index=(
                            paragraph.paragraph_index
                        )
                    )
                )

        return errors