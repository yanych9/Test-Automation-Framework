"""Assertion helpers for medical AI model API testing.

The goal of this module is to demonstrate how AI model service APIs can be
validated with more than status-code assertions. In a medical AI scenario, the
response should usually be checked from several dimensions:

- required fields are present;
- probability values are within a valid range;
- risk levels belong to a controlled vocabulary;
- traceability fields such as request_id and model_version exist.
"""

from __future__ import annotations

from typing import Any, Iterable, Mapping, Sequence


class MedicalAssertionError(AssertionError):
    """Raised when a medical AI API response fails validation."""


def get_by_path(data: Mapping[str, Any], dotted_path: str) -> Any:
    """Read nested data with a dotted path.

    Example:
        get_by_path(response, "result.probability")
    """
    current: Any = data
    for part in dotted_path.split("."):
        if not isinstance(current, Mapping) or part not in current:
            raise MedicalAssertionError(f"Missing field path: {dotted_path}")
        current = current[part]
    return current


def assert_required_fields(data: Mapping[str, Any], required_fields: Iterable[str]) -> None:
    """Assert that all required dotted-path fields exist."""
    for field in required_fields:
        get_by_path(data, field)


def assert_probability_range(value: Any, allowed_range: Sequence[float]) -> None:
    """Assert model probability is numeric and in the expected range."""
    if len(allowed_range) != 2:
        raise MedicalAssertionError("probability_range must contain [min, max]")

    lower, upper = allowed_range
    if not isinstance(value, (int, float)):
        raise MedicalAssertionError(f"Probability must be numeric, got {type(value).__name__}")

    if not lower <= float(value) <= upper:
        raise MedicalAssertionError(
            f"Probability {value} is out of range [{lower}, {upper}]"
        )


def assert_enum_value(value: Any, allowed_values: Iterable[Any], field_name: str) -> None:
    """Assert a field value belongs to a controlled vocabulary."""
    allowed = list(allowed_values)
    if value not in allowed:
        raise MedicalAssertionError(
            f"{field_name}={value!r} is not in allowed values: {allowed}"
        )


def assert_message_contains(data: Mapping[str, Any], expected_keyword: str) -> None:
    """Assert error message contains the expected keyword."""
    message = str(data.get("message", ""))
    if expected_keyword not in message:
        raise MedicalAssertionError(
            f"Expected message to contain {expected_keyword!r}, got {message!r}"
        )


def validate_medical_ai_response(response_json: Mapping[str, Any], expected: Mapping[str, Any]) -> None:
    """Validate a medical AI response according to YAML-defined rules."""
    required_fields = expected.get("required_fields", [])
    assert_required_fields(response_json, required_fields)

    if "probability_path" in expected:
        probability = get_by_path(response_json, expected["probability_path"])
        assert_probability_range(probability, expected.get("probability_range", [0, 1]))

    if "risk_level_path" in expected:
        risk_level = get_by_path(response_json, expected["risk_level_path"])
        assert_enum_value(
            risk_level,
            expected.get("allowed_risk_levels", ["low", "medium", "high"]),
            "risk_level",
        )

    if "message_contains" in expected:
        assert_message_contains(response_json, expected["message_contains"])
