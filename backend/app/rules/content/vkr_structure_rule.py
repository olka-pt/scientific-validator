from backend.app.models.document import (
    DocumentModel,
)

from backend.app.models.validation import (
    ValidationError,
)

from backend.app.rules.base_rule import (
    BaseRule,
)

from backend.app.config.semantic_types import (
    TITLE_PAGE,
    ASSIGNMENT,
    ABSTRACT_RU,
    ABSTRACT_EN,
    CONTENTS,
    INTRODUCTION,
    ANALYTICAL_SECTION,
    SPECIAL_SECTION,
    LIFE_SAFETY_SECTION,
    ECONOMIC_EFFICIENCY_SECTION,
    CONCLUSION,
    REFERENCES_HEADER,
)


class VkrStructureRule(BaseRule):

    REQUIRED_STRUCTURE = [

        TITLE_PAGE,
        ASSIGNMENT,

        ABSTRACT_RU,
        ABSTRACT_EN,

        CONTENTS,

        INTRODUCTION,

        ANALYTICAL_SECTION,
        SPECIAL_SECTION,
        LIFE_SAFETY_SECTION,
        ECONOMIC_EFFICIENCY_SECTION,

        CONCLUSION,

        REFERENCES_HEADER,
    ]

    def check(
        self,
        document: DocumentModel,
    ) -> list[ValidationError]:

        errors = []

        found_sections = []

        for paragraph in document.paragraphs:

            semantic_type = (
                paragraph.semantic_type
            )

            if (
                semantic_type
                in self.REQUIRED_STRUCTURE
                and semantic_type not in found_sections
            ):

                found_sections.append(
                    semantic_type
                )

        for required_section in (
            self.REQUIRED_STRUCTURE
        ):

            if required_section not in found_sections:

                errors.append(
                    ValidationError(
                        category="structure",

                        message=(
                            "Отсутствует обязательный раздел ВКР"
                        ),

                        expected=required_section,

                        actual="Не найден",

                        paragraph_index=-1,

                        severity="critical",
                    )
                )

        previous_index = -1

        for section in found_sections:

            current_index = (
                self.REQUIRED_STRUCTURE.index(
                    section
                )
            )

            if current_index < previous_index:

                errors.append(
                    ValidationError(
                        category="structure",

                        message=(
                            "Нарушен порядок разделов ВКР"
                        ),

                        expected="Корректный порядок",

                        actual=section,

                        paragraph_index=-1,

                        severity="critical",
                    )
                )

            previous_index = current_index

        return errors