"""Application-controlled Issue Triage workflow shared by CLI and Streamlit demos (R5, R6)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from openai import OpenAI

from prompts import build_messages

try:
    from demo_common import call_with_retry
except ImportError:
    def call_with_retry(fn):
        return fn()

# Single Source of Truth for component owners
COMPONENT_OWNERS: dict[str, str] = {
    "payment": "checkout-platform",
    "identity": "identity-platform",
    "search": "search-platform",
}

# Strict JSON Schema tool specification (R5)
FUNCTION_TOOLS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "get_component_owner",
            "description": (
                "Tra cứu team kỹ thuật chịu trách nhiệm cho một software component. "
                "Chỉ đọc, an toàn, không có tác dụng phụ (read-only, idempotent). "
                "Chỉ chấp nhận các component trong allowlist: payment, identity, search."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "component": {
                        "type": "string",
                        "enum": list(COMPONENT_OWNERS.keys()),
                        "description": "Tên component cần tra cứu: payment, identity hoặc search.",
                    }
                },
                "required": ["component"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    }
]


@dataclass(frozen=True)
class ToolTrace:
    """One validated tool request and the application execution result returned to the model."""

    call_id: str
    name: str
    arguments: dict[str, Any]
    result: dict[str, Any]


@dataclass(frozen=True)
class TriageResult:
    """Consumer-facing result of a complete, 4-stage Issue Triage agent loop."""

    tool_traces: tuple[ToolTrace, ...]
    final_response: str
    messages: tuple[dict[str, Any], ...]


def get_component_owner(component: str) -> str:
    """Lookup owner strictly within application boundary."""
    return COMPONENT_OWNERS[component]


def execute_tool_call(name: str, raw_arguments: str | dict[str, Any]) -> dict[str, Any]:
    """Validate a requested tool call and arguments at the application layer.
    
    Treats the model's tool proposal as untrusted input.
    Validates tool name against allowlist, parses JSON, and verifies domain constraints.
    Returns a result dict (with 'error' key upon validation failure) rather than crashing.
    """
    if name != "get_component_owner":
        return {
            "error": f"Tool không được cấp phép: '{name}'.",
            "allowed_tools": ["get_component_owner"],
        }

    if isinstance(raw_arguments, str):
        try:
            arguments = json.loads(raw_arguments)
        except Exception as err:
            return {"error": f"Đối số tool không phải JSON hợp lệ: {err}"}
    elif isinstance(raw_arguments, dict):
        arguments = raw_arguments
    else:
        return {"error": "Định dạng đối số tool không hợp lệ."}

    if not isinstance(arguments, dict):
        return {"error": "Đối số tool phải là một JSON object."}

    component = arguments.get("component")
    if not component or not isinstance(component, str):
        return {
            "error": "Thiếu tham số bắt buộc 'component' kiểu chuỗi.",
            "allowed_components": list(COMPONENT_OWNERS.keys()),
        }

    component = component.strip().lower()
    if component not in COMPONENT_OWNERS:
        return {
            "error": f"Component '{component}' không tồn tại trong allowlist hệ thống.",
            "allowed_components": list(COMPONENT_OWNERS.keys()),
        }

    return {
        "component": component,
        "owner": get_component_owner(component),
        "status": "success",
    }


def triage_issue(
    client: OpenAI,
    model: str,
    issue: str,
    force_tool: bool = True,
) -> TriageResult:
    """Triage one issue via application-controlled function calling (4-stage trace).
    
    Stage 1: Model proposes tool call
    Stage 2: Application validates and executes tool
    Stage 3: Tool result is fed back to model
    Stage 4: Model delivers final natural language triage
    """
    system_note = (
        "Khi cần xác định team kỹ thuật phụ trách cho một component, "
        "bắt buộc gọi function get_component_owner. "
        "Không tự bịa ra thông tin team phụ trách."
    )
    messages: list[dict[str, Any]] = build_messages(issue, additional_system_note=system_note)

    # First call: ask model to analyze issue and trigger tool call
    first_response = call_with_retry(
        lambda: client.chat.completions.create(
            model=model,
            messages=messages,
            tools=FUNCTION_TOOLS,
            tool_choice="required" if force_tool else "auto",
        )
    )

    assistant_msg = first_response.choices[0].message
    tool_calls = assistant_msg.tool_calls or []
    if not tool_calls:
        # If model somehow didn't return tool calls, record and return prose
        return TriageResult(
            tool_traces=(),
            final_response=assistant_msg.content or "(Model không trả về nội dung hay tool call nào.)",
            messages=tuple(messages),
        )

    messages.append(assistant_msg)

    traces: list[ToolTrace] = []
    for tc in tool_calls:
        func_name = tc.function.name
        func_args_raw = tc.function.arguments
        try:
            parsed_args = json.loads(func_args_raw) if isinstance(func_args_raw, str) else func_args_raw
        except Exception:
            parsed_args = {"raw": str(func_args_raw)}

        # Application executes tool safely
        exec_result = execute_tool_call(func_name, func_args_raw)

        traces.append(
            ToolTrace(
                call_id=tc.id,
                name=func_name,
                arguments=parsed_args if isinstance(parsed_args, dict) else {"value": parsed_args},
                result=exec_result,
            )
        )

        messages.append(
            {
                "role": "tool",
                "tool_call_id": tc.id,
                "content": json.dumps(exec_result, ensure_ascii=False),
            }
        )

    # Final call: model receives tool result and responds with final answer
    final_response = call_with_retry(
        lambda: client.chat.completions.create(
            model=model,
            messages=messages,
            tools=FUNCTION_TOOLS,
            tool_choice="none",  # Do not force tool loop again
        )
    )

    final_text = final_response.choices[0].message.content or "(Model không trả về văn bản kết luận.)"

    return TriageResult(
        tool_traces=tuple(traces),
        final_response=final_text,
        messages=tuple(messages),
    )
