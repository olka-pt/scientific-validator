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


class InstitutionalEmailRule(BaseRule):

    EMAIL_PATTERN = (
        r"[a-zA-Z0-9._%+-]+"
        r"@"
        r"[a-zA-Z0-9.-]+"
        r"\.[a-zA-Z]{2,}"
    )

    PUBLIC_EMAIL_DOMAINS = {
        "gmail.com",
        "yahoo.com",
        "hotmail.com",
        "outlook.com",
        "mail.ru",
        "bk.ru",
        "list.ru",
        "inbox.ru",
        "yandex.ru"
    }

    def check(
        self,
        document: DocumentModel
    ) -> list[ValidationError]:

        errors = []

        for paragraph in (
            document.paragraphs
        ):

            emails = re.findall(
                self.EMAIL_PATTERN,
                paragraph.text
            )

            for email in emails:

                domain = (
                    email.split("@")[-1]
                    .lower()
                )

                if (
                    domain
                    in self.PUBLIC_EMAIL_DOMAINS
                ):

                    errors.append(
                        ValidationError(
                            category="authors",

                            message=(
                                "Публичные почтовые домены запрещены"
                            ),

                            expected=(
                                "Адрес корпоративной электронной почты"
                            ),

                            actual=email,

                            paragraph_index=(
                                paragraph.paragraph_index
                            )
                        )
                    )

        return errors