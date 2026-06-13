def is_within_tolerance(
    actual: float,
    expected: float,
    tolerance: float = 0.5
) -> bool:

    return (
        abs(actual - expected)
        <= tolerance
    )