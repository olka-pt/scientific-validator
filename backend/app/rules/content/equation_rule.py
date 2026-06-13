import re

from backend.app.models.document import DocumentModel
from backend.app.models.validation import ValidationError
from backend.app.rules.base_rule import BaseRule
from backend.app.config.semantic_types import EQUATION
from backend.app.config.style_rules import EXPECTED_FONT_SIZES, EXPECTED_ALIGNMENTS


class EquationRule(BaseRule):
    """
    Полная проверка формул:
    - semantic_type = EQUATION
    - последовательность номеров (1), (2), ...
    - выравнивание по центру
    - проверка шрифта и размера
    """

    def __init__(
        self,
        font_family: str | None = None,
        font_size: float | None = None
    ):
        self.font_family = font_family
        self.font_size = font_size

    def check(self, document: DocumentModel) -> list[ValidationError]:
        errors = []
        expected_number = 1  # первый номер формулы

        for paragraph in document.paragraphs:
            if paragraph.semantic_type != EQUATION:
                continue

            text = paragraph.text.strip()

            # Номер формулы
            match = re.search(r"\((\d+)\)", text)
            if not match:
                errors.append(
                    ValidationError(
                        category="equation",
                        message="Отсутствует номер формулы",
                        expected=f"({expected_number})",
                        actual=text[:20] + "...",
                        paragraph_index=paragraph.paragraph_index
                    )
                )
            else:
                num = int(match.group(1))
                if num != expected_number:
                    errors.append(
                        ValidationError(
                            category="equation",
                            message="Нарушена последовательность нумерации формул",
                            expected=f"Ожидалась формула ({expected_number})",
                            actual=f"({num})",
                            paragraph_index=paragraph.paragraph_index
                        )
                    )
                expected_number += 1

            # Проверка выравнивания
            if paragraph.alignment != EXPECTED_ALIGNMENTS.get(EQUATION, "center"):
                errors.append(
                    ValidationError(
                        category="equation",
                        message="Формула должна быть выровнена по центру",
                        expected="по центру",
                        actual=str(paragraph.alignment),
                        paragraph_index=paragraph.paragraph_index
                    )
                )

            # Проверка размера шрифта
            if self.font_size and paragraph.font_size != self.font_size:
                errors.append(
                    ValidationError(
                        category="equation",
                        message="Неверный размер шрифта формулы",
                        expected=str(self.font_size),
                        actual=str(paragraph.font_size),
                        paragraph_index=paragraph.paragraph_index
                    )
                )

            # Проверка шрифта
            if self.font_family and paragraph.font_family != self.font_family:
                errors.append(
                    ValidationError(
                        category="equation",
                        message="Неверный шрифт формулы",
                        expected=str(self.font_family),
                        actual=str(paragraph.font_family),
                        paragraph_index=paragraph.paragraph_index
                    )
                )

        return errors