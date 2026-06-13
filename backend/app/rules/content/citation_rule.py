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


CITATION_PATTERN = (
    r"\[(\d+(?:\s*[-,]\s*\d+)*)\]"
)


class CitationRule(BaseRule):

    def check(
        self,
        document: DocumentModel
    ) -> list[ValidationError]:

        errors = []

        reference_numbers = set()

        for paragraph in (
            document.paragraphs
        ):

            if (
                paragraph.semantic_type
                == "reference_item"
            ):

                match = re.match(
                    r"^(\d+)\.",
                    paragraph.text.strip()
                )

                if match:

                    reference_numbers.add(
                        int(match.group(1))
                    )

        for paragraph in (
            document.paragraphs
        ):

            if (
                paragraph.semantic_type
                == "reference_item"
            ):
                continue

            matches = re.findall(
                CITATION_PATTERN,
                paragraph.text
            )

            parsed_numbers = []

            for match in matches:

                parts = match.split(",")

                for part in parts:

                    part = part.strip()

                    if "-" in part:

                        try:

                            start, end = (
                                part.split("-")
                            )

                            start = int(
                                start.strip()
                            )

                            end = int(
                                end.strip()
                            )

                            for number in range(
                                start,
                                end + 1
                            ):

                                parsed_numbers.append(
                                    number
                                )

                        except ValueError:

                            errors.append(
                                ValidationError(
                                    category="citations",

                                    message=(
                                        "Некорректный диапазон ссылки"
                                    ),

                                    expected=(
                                        "Например: [1–3]"
                                    ),

                                    actual=part,

                                    paragraph_index=(
                                        paragraph.paragraph_index
                                    )
                                )
                            )

                    else:

                        if not part.isdigit():

                            errors.append(
                                ValidationError(
                                    category="citations",

                                    message=(
                                        "Некорректный формат ссылки"
                                    ),

                                    expected="Номер источника",

                                    actual=part,

                                    paragraph_index=(
                                        paragraph.paragraph_index
                                    )
                                )
                            )

                            continue

                        parsed_numbers.append(
                            int(part)
                        )

            for citation_number in (
                parsed_numbers
            ):

                if (
                    citation_number
                    not in reference_numbers
                ):

                    errors.append(
                        ValidationError(
                            category="citations",

                            message=(
                                "Ссылка указывает на отсутствующий источник"
                            ),

                            expected=(
                                "Существующий источник"
                            ),

                            actual=str(
                                citation_number
                            ),

                            paragraph_index=(
                                paragraph.paragraph_index
                            )
                        )
                    )

        return errors