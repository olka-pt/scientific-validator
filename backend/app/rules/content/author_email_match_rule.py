# backend/app/rules/content/author_email_match_rule.py

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

from backend.app.config.semantic_types import (
    AUTHORS
)


class AuthorEmailMatchRule(BaseRule):

    EMAIL_PATTERN = (
        r"[a-zA-Z0-9._%+-]+"
        r"@"
        r"[a-zA-Z0-9.-]+"
        r"\.[a-zA-Z]{2,}"
    )

    CYRILLIC_PATTERN = re.compile(
        r"[а-яА-Я]"
    )

    AUTHOR_PATTERN = re.compile(
        r"(?:"
        r"[А-ЯA-Z][а-яa-z\-]+"
        r"\s+"
        r"[А-ЯA-Z]\."
        r"\s*"
        r"[А-ЯA-Z]\."
        r"(?:[\d¹²³⁴⁵⁶⁷⁸⁹, ]+)?"
        r")"
    )

    def check(
        self,
        document: DocumentModel
    ) -> list[ValidationError]:

        errors = []

        authors = []

        emails = []

        for paragraph in (
            document.paragraphs
        ):

            # Count ONLY Russian author block
            # to avoid bilingual duplication

            if (
                paragraph.semantic_type
                == AUTHORS

                and

                self.CYRILLIC_PATTERN.search(
                    paragraph.text
                )
            ):

                found_authors = re.findall(
                    self.AUTHOR_PATTERN,
                    paragraph.text
                )


                cleaned_authors = [
                    author.strip()
                    for author in found_authors
                    if author.strip()
                ]

                authors.extend(
                    cleaned_authors
                )


            found_emails = re.findall(
                self.EMAIL_PATTERN,
                paragraph.text
            )

            emails.extend(
                found_emails
            )

        unique_emails = list(
            set(emails)
        )

        if (
            len(authors)
            !=
            len(unique_emails)
        ):

            errors.append(
                ValidationError(
                    category="authors",

                    message=(
                        "Количество авторов не совпадает с количеством электронных адресов"
                    ),

                    expected=str(
                        f"Авторов: {len(authors)}"
                    ),

                    actual=str(
                        f"Email: {len(unique_emails)}"
                    ),

                    paragraph_index=-1
                )
            )

        for email in unique_emails:

            if not re.fullmatch(
                self.EMAIL_PATTERN,
                email
            ):

                errors.append(
                    ValidationError(
                        category="authors",

                        message=(
                            "Некорректный формат электронной почты"
                        ),

                        expected=(
                            "Корректный адрес электронной почты"
                        ),

                        actual=email,

                        paragraph_index=-1
                    )
                )

        return errors