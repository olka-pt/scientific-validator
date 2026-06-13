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


class EmailFormatRule(BaseRule):

    EMAIL_PATTERN = (
        r"^[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+"
        r"\.[A-Za-z]{2,}$"
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
                != "email"
            ):
                continue

            text = (
                paragraph.text
            )

            emails = [
                email.strip()
                for email in (
                    text.split(",")
                )
                if email.strip()
            ]

            for email in emails:

                is_valid = re.match(
                    self.EMAIL_PATTERN,
                    email
                )

                if not is_valid:

                    errors.append(
                        ValidationError(
                            category="email",

                            message=(
                                "Некорректный формат электронной почты"
                            ),

                            expected=(
                                "Корректный адрес электронной почты"
                            ),

                            actual=email,

                            paragraph_index=(
                                paragraph.paragraph_index
                            )
                        )
                    )

        return errors