# backend/app/models/validation.py

from pydantic import BaseModel


class ValidationError(BaseModel):

    category: str

    message: str

    expected: str
    actual: str

    paragraph_index: int | None = None

    severity: str = "warning"


class ValidationResult(BaseModel):

    total_checks: int

    total_errors: int

    score: float

    errors: list[ValidationError]

    critical_errors_count: int = 0

    regular_errors_count: int = 0

    warnings_count: int = 0

    recommendations_count: int = 0

    weighted_penalty: float = 0.0

    has_critical_errors: bool = False

    status: str = "Соответствует требованиям"