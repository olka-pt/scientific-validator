from backend.app.models.validation import (
    ValidationResult
)


class ValidationRecommendationEngine:

    def __init__(
        self,
        result: ValidationResult
    ):

        self.result = result

    def generate(
        self
    ) -> list[str]:

        recommendations = []

        for error in self.result.errors:

            recommendation = (
                self._generate_single(
                    error
                )
            )

            if recommendation:

                recommendations.append(
                    recommendation
                )

        return list(
            dict.fromkeys(
                recommendations
            )
        )

    def _generate_single(
        self,
        error
    ) -> str | None:

        message = (
            error.message
            .lower()
        )

        category = (
            error.category
            .lower()
        )

        if (
            "authors count"
            in message
        ):

            expected = (
                error.expected
            )

            actual = (
                error.actual
            )

            return (
                f"Количество авторов и email должно совпадать "
                f"(сейчас {actual}, ожидается {expected})"
            )

        if (
            "references"
            in message
        ):

            return (
                "Добавьте раздел Источники / References"
            )

        if (
            "equation"
            in category
        ):

            return (
                "Проверьте оформление формул и наличие ссылок на них"
            )

        if (
            "table"
            in category
        ):

            return (
                "Проверьте размер шрифта внутри таблиц (10–12 пт)"
            )

        if (
            "font"
            in message
        ):

            return (
                "Приведите размеры шрифта к требованиям шаблона"
            )

        if (
            "margin"
            in message
        ):

            return (
                "Проверьте размеры полей документа"
            )

        if (
            "section"
            in category
        ):

            return (
                "Проверьте структуру разделов документа"
            )

        return (
            f"Исправить: {error.message}"
        )