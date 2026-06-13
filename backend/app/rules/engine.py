# backend/app/rules/engine.py

from backend.app.models.document import (
    DocumentModel
)

from backend.app.models.validation import (
    ValidationResult
)

from backend.app.rules.base_rule import (
    BaseRule
)


class RuleEngine:

    SEVERITY_WEIGHTS = {
        "critical": 10.0,
        "error": 3.0,
        "warning": 1.0,
        "recommendation": 0.3,
    }

    def __init__(
        self,
        rules: list[BaseRule]
    ):

        self.rules = rules

    def validate(
        self,
        document: DocumentModel
    ) -> ValidationResult:

        all_errors = []

        total_checks = 0

        for rule in self.rules:

            errors = rule.check(
                document
            )

            all_errors.extend(
                errors
            )

            total_checks += len(
                document.paragraphs
            )

        total_errors = len(
            all_errors
        )

        critical_errors_count = self._count_by_severity(
            all_errors,
            "critical",
        )

        regular_errors_count = self._count_by_severity(
            all_errors,
            "error",
        )

        warnings_count = self._count_by_severity(
            all_errors,
            "warning",
        )

        recommendations_count = self._count_by_severity(
            all_errors,
            "recommendation",
        )

        weighted_penalty = self._calculate_weighted_penalty(
            all_errors
        )

        score = self._calculate_score(
            weighted_penalty=weighted_penalty,
        )

        has_critical_errors = (
            critical_errors_count > 0
        )

        status = self._get_status(
            score=score,
            has_critical_errors=has_critical_errors,
        )

        return ValidationResult(
            total_checks=total_checks,
            total_errors=total_errors,
            score=score,
            errors=all_errors,
            critical_errors_count=critical_errors_count,
            regular_errors_count=regular_errors_count,
            warnings_count=warnings_count,
            recommendations_count=recommendations_count,
            weighted_penalty=weighted_penalty,
            has_critical_errors=has_critical_errors,
            status=status,
        )

    @classmethod
    def _calculate_weighted_penalty(
        cls,
        errors,
    ) -> float:

        penalty = 0.0

        for error in errors:

            severity = getattr(
                error,
                "severity",
                "warning",
            )

            penalty += cls.SEVERITY_WEIGHTS.get(
                severity,
                1.0,
            )

        return round(
            penalty,
            2,
        )

    @staticmethod
    def _calculate_score(
        weighted_penalty: float,
    ) -> float:

        score = (
            100
            - weighted_penalty
        )

        if score < 0:
            score = 0

        return round(
            score,
            2,
        )

    @staticmethod
    def _count_by_severity(
        errors,
        severity: str,
    ) -> int:

        return sum(
            1
            for error in errors
            if getattr(
                error,
                "severity",
                "warning",
            ) == severity
        )

    @staticmethod
    def _get_status(
        score: float,
        has_critical_errors: bool,
    ) -> str:

        if has_critical_errors:
            return "Не соответствует требованиям"

        if score >= 95:
            return "Соответствует требованиям"

        if score >= 80:
            return "Требует доработки"

        return "Не соответствует требованиям"