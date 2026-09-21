"""Offline test suite for application-side tool execution and security boundary (R5)."""

import json
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "draft" / "d02-3" / "scripts"
if not SCRIPTS_DIR.exists():
    SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from triage_workflow import COMPONENT_OWNERS, FUNCTION_TOOLS, execute_tool_call


def test_valid_components():
    """Valid components must return the correct team owner."""
    for comp, expected_owner in COMPONENT_OWNERS.items():
        res = execute_tool_call("get_component_owner", json.dumps({"component": comp}))
        assert "error" not in res
        assert res["component"] == comp
        assert res["owner"] == expected_owner


def test_invalid_component_handled_gracefully():
    """Unknown components must return an error dict and not raise unhandled exceptions."""
    res = execute_tool_call("get_component_owner", json.dumps({"component": "analytics"}))
    assert "error" in res
    assert "allowlist" in res["error"]
    assert "allowed_components" in res


def test_unknown_tool_rejected():
    """Unapproved tool names must be rejected."""
    res = execute_tool_call("delete_database", "{}")
    assert "error" in res
    assert "Tool không được cấp phép" in res["error"]


def test_malformed_json_arguments():
    """Malformed JSON arguments must return an error dict and not crash."""
    res = execute_tool_call("get_component_owner", "{broken_json")
    assert "error" in res
    assert "không phải JSON hợp lệ" in res["error"]


def test_tool_spec_synced_with_owners():
    """Tool specification enum must match COMPONENT_OWNERS keys exactly."""
    tool_def = FUNCTION_TOOLS[0]["function"]
    schema_enum = tool_def["parameters"]["properties"]["component"]["enum"]
    assert set(schema_enum) == set(COMPONENT_OWNERS.keys())
