"""Offline test suite for IssueTriage Pydantic schema and application invariants (R3, R4)."""

import sys
from pathlib import Path
import pytest
from pydantic import ValidationError

# Ensure scripts directory is on sys.path
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "draft" / "d02-3" / "scripts"
if not SCRIPTS_DIR.exists():
    SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from schemas import IssueTriage


def test_valid_classified_payload():
    """Valid classified payload should parse cleanly without error."""
    payload = {
        "status": "classified",
        "severity": "P0",
        "component": "payment",
        "needs_urgent_response": True,
        "reason": "Payment service down for all credit cards.",
    }
    triage = IssueTriage.model_validate(payload)
    assert triage.status == "classified"
    assert triage.severity == "P0"
    assert triage.component == "payment"
    assert triage.needs_urgent_response is True


def test_valid_out_of_scope_payload():
    """Out of scope issues do not require component or severity."""
    payload = {
        "status": "out_of_scope",
        "reason": "This is a general marketing inquiry, not a software issue.",
    }
    triage = IssueTriage.model_validate(payload)
    assert triage.status == "out_of_scope"
    assert triage.severity is None
    assert triage.component is None
    assert triage.needs_urgent_response is False


def test_invalid_severity_enum():
    """Invalid severity enum values (e.g. 'Critical', 'high', 'P5') must be rejected."""
    payload = {
        "status": "classified",
        "severity": "Critical",
        "component": "payment",
        "needs_urgent_response": True,
        "reason": "Critical outage.",
    }
    with pytest.raises(ValidationError) as exc:
        IssueTriage.model_validate(payload)
    assert "severity" in str(exc.value)


def test_invalid_component_enum():
    """Components outside {payment, identity, search} must be rejected."""
    payload = {
        "status": "classified",
        "severity": "P1",
        "component": "billing",
        "needs_urgent_response": False,
        "reason": "Billing component issue.",
    }
    with pytest.raises(ValidationError) as exc:
        IssueTriage.model_validate(payload)
    assert "component" in str(exc.value)


def test_extra_fields_forbidden():
    """Extra fields must be rejected (extra='forbid')."""
    payload = {
        "status": "classified",
        "severity": "P2",
        "component": "search",
        "needs_urgent_response": False,
        "reason": "Search is a bit slow.",
        "unexpected_field": "injected_value",
    }
    with pytest.raises(ValidationError) as exc:
        IssueTriage.model_validate(payload)
    assert "extra" in str(exc.value).lower()


def test_missing_required_field():
    """Missing required field ('reason') must be rejected."""
    payload = {
        "status": "classified",
        "severity": "P1",
        "component": "identity",
        "needs_urgent_response": False,
    }
    with pytest.raises(ValidationError) as exc:
        IssueTriage.model_validate(payload)
    assert "reason" in str(exc.value)


def test_cross_field_invariant_p0_requires_urgent():
    """Cross-field invariant: severity=P0 but needs_urgent_response=False must be rejected."""
    payload = {
        "status": "classified",
        "severity": "P0",
        "component": "payment",
        "needs_urgent_response": False,
        "reason": "System is completely halted.",
    }
    with pytest.raises(ValidationError) as exc:
        IssueTriage.model_validate(payload)
    assert "needs_urgent_response bắt buộc phải là True" in str(exc.value)


def test_classified_requires_severity_and_component():
    """When status='classified', omitting severity or component must be rejected."""
    payload = {
        "status": "classified",
        "severity": None,
        "component": "payment",
        "needs_urgent_response": False,
        "reason": "Valid reason.",
    }
    with pytest.raises(ValidationError) as exc:
        IssueTriage.model_validate(payload)
    assert "severity" in str(exc.value)
