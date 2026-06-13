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


class AuthorAffiliationMatchRule(BaseRule):

    INDEX_PATTERN = (
        r"\^?(\d+(?:\s*,\s*\d+)*)"
        r"|([¹²³⁴⁵⁶⁷⁸⁹]+)"
        r"|([¹²³⁴⁵⁶⁷⁸⁹](?:\s*,\s*[¹²³⁴⁵⁶⁷⁸⁹])+)"
    )

    SUPERSCRIPT_MAP = {
        "¹": 1,
        "²": 2,
        "³": 3,
        "⁴": 4,
        "⁵": 5,
        "⁶": 6,
        "⁷": 7,
        "⁸": 8,
        "⁹": 9
    }

    def _extract_indices(
        self,
        text: str
    ) -> set[int]:

        indices = set()

        matches = re.findall(
            self.INDEX_PATTERN,
            text
        )

        for (
            numeric_index,
            superscript_index,
            superscript_comma_block
        ) in matches:

            if numeric_index:

                parts = re.split(
                    r"\s*,\s*",
                    numeric_index
                )

                for part in parts:

                    if part.isdigit():

                        indices.add(
                            int(part)
                        )

            if superscript_index:

                for symbol in (
                    superscript_index
                ):

                    normalized = (
                        self.SUPERSCRIPT_MAP.get(
                            symbol
                        )
                    )

                    if normalized:

                        indices.add(
                            normalized
                        )

            if superscript_comma_block:

                cleaned = re.split(
                    r"\s*,\s*",
                    superscript_comma_block
                )

                for symbol in cleaned:

                    normalized = (
                        self.SUPERSCRIPT_MAP.get(
                            symbol
                        )
                    )

                    if normalized:

                        indices.add(
                            normalized
                        )                        
        return indices

    def check(
        self,
        document: DocumentModel
    ) -> list[ValidationError]:

        errors = []

        author_indices = set()

        affiliation_indices = set()

        for paragraph in (
            document.paragraphs
        ):

            text = (
                paragraph.text
            )

            if (
                paragraph.semantic_type
                == "author"
            ):

                extracted = (
                    self._extract_indices(
                        text
                    )
                )

                author_indices.update(
                    extracted
                )

            if (
                paragraph.semantic_type
                == "affiliation"
            ):

                extracted = (
                    self._extract_indices(
                        text
                    )
                )

                affiliation_indices.update(
                    extracted
                )

        missing_indices = (
            author_indices
            - affiliation_indices
        )

        if missing_indices:

            errors.append(
                ValidationError(
                    category="affiliation",

                    message=(
                        "Автор ссылается на несуществующую организацию"
                    ),

                    expected=(
                        "Существующий индекс организации"
                    ),

                    actual=str(
                        sorted(
                            missing_indices
                        )
                    ),

                    paragraph_index=-1
                )
            )

        return errors