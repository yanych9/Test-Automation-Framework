"""Example pytest cases for a disease prediction API.

These cases demonstrate how the original interface automation framework can be
extended to a medical AI model-service scenario.

Notes for interview explanation:
- The API endpoint is a demo endpoint and requires a local/mock service to run.
- The focus of this file is YAML-driven case loading and medical-AI-specific
  assertion design.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import pytest
import requests
import yaml

from medical_ai_extension.utils.medical_assertions import validate_medical_ai_response

BASE_DIR = Path(__file__).resolve().parents[1]
CASE_FILE = BASE_DIR / "testcases" / "disease_predict_cases.yaml"
ENV_FILE = BASE_DIR / "config" / "medical_env.yaml"


def load_yaml(path: Path) -> Any:
    """Load a YAML file safely."""
    with path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def load_cases() -> List[Dict[str, Any]]:
    """Load disease prediction API cases from YAML."""
    return load_yaml(CASE_FILE)


def load_env() -> Dict[str, Any]:
    """Load medical AI test environment config."""
    return load_yaml(ENV_FILE)


@pytest.mark.parametrize("case", load_cases(), ids=lambda item: item["case_id"])
def test_disease_prediction_api(case: Dict[str, Any]) -> None:
    """Validate disease prediction API with YAML-defined rules."""
    env = load_env()
    service = env["service"]
    url = service["base_url"].rstrip("/") + case["path"]

    response = requests.request(
        method=case["method"],
        url=url,
        json=case.get("request", {}),
        headers=service.get("default_headers", {}),
        timeout=service.get("timeout", 5),
    )

    expected = case["expected"]
    assert response.status_code == expected["status_code"]

    response_json = response.json()
    validate_medical_ai_response(response_json, expected)


def test_medical_ai_assertion_demo_without_http() -> None:
    """A pure assertion demo that can run without a backend service.

    This test is useful for showing the medical-AI-specific assertion logic
    even when no local disease prediction service is available.
    """
    response_json = {
        "request_id": "REQ_DEMO_001",
        "model_name": "disease-risk-demo",
        "model_version": "v1.0.0",
        "result": {
            "risk_level": "high",
            "probability": 0.86,
        },
    }
    expected = {
        "required_fields": [
            "request_id",
            "model_name",
            "model_version",
            "result.risk_level",
            "result.probability",
        ],
        "probability_path": "result.probability",
        "probability_range": [0, 1],
        "risk_level_path": "result.risk_level",
        "allowed_risk_levels": ["low", "medium", "high"],
    }

    validate_medical_ai_response(response_json, expected)
