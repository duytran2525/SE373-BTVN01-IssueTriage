"""Offline mock test for 4-stage Agentic tool loop (R6)."""

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "draft" / "d02-3" / "scripts"
if not SCRIPTS_DIR.exists():
    SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from triage_workflow import triage_issue


@dataclass
class MockFunction:
    name: str
    arguments: str


@dataclass
class MockToolCall:
    id: str
    function: MockFunction


@dataclass
class MockMessage:
    content: str | None
    tool_calls: list[MockToolCall] | None = None
    role: str = "assistant"

    def __getitem__(self, item: str):
        return getattr(self, item)


@dataclass
class MockChoice:
    message: MockMessage


@dataclass
class MockResponse:
    choices: list[MockChoice]


class FakeOpenAIClient:
    """Mock OpenAI client to test tool loop offline without external network calls."""

    def __init__(self):
        self.call_count = 0
        self.recorded_messages = []
        self.chat = self

    @property
    def completions(self):
        return self

    def create(self, **kwargs):
        self.call_count += 1
        messages = kwargs.get("messages", [])
        self.recorded_messages.append(messages)

        if self.call_count == 1:
            # Round 1: Model proposes a tool call
            tool_call = MockToolCall(
                id="call_mock_12345",
                function=MockFunction(
                    name="get_component_owner",
                    arguments=json.dumps({"component": "payment"}),
                ),
            )
            return MockResponse(
                choices=[
                    MockChoice(
                        message=MockMessage(
                            content=None,
                            tool_calls=[tool_call],
                        )
                    )
                ]
            )
        else:
            # Round 2: Model receives tool result and produces final answer
            return MockResponse(
                choices=[
                    MockChoice(
                        message=MockMessage(
                            content="Issue thuộc phân hệ Payment. Team phụ trách là checkout-platform.",
                            tool_calls=None,
                        )
                    )
                ]
            )


def test_4_stage_agent_tool_loop():
    """Verify that the 4-stage tool loop executes correctly offline:
    Stage 1: tool_call proposal
    Stage 2: application executes tool
    Stage 3: tool_result returned with matching call_id
    Stage 4: final response delivered
    """
    fake_client = FakeOpenAIClient()
    issue_text = "Thanh toán thất bại từ 14:00."

    result = triage_issue(
        client=fake_client,
        model="fake-model",
        issue=issue_text,
        force_tool=True,
    )

    # 1. Check tool trace exists
    assert len(result.tool_traces) == 1
    trace = result.tool_traces[0]

    # Stage 1 verification: Tool proposal
    assert trace.call_id == "call_mock_12345"
    assert trace.name == "get_component_owner"
    assert trace.arguments == {"component": "payment"}

    # Stage 2 & 3 verification: Application execution and result
    assert trace.result["component"] == "payment"
    assert trace.result["owner"] == "checkout-platform"

    # Stage 4 verification: Final response
    assert "checkout-platform" in result.final_response

    # Verify conversation message sequence
    # Expect: system -> user -> assistant (tool_calls) -> tool (tool_result)
    round_2_messages = fake_client.recorded_messages[1]
    assert len(round_2_messages) >= 4
    assert round_2_messages[0]["role"] == "system"
    assert round_2_messages[1]["role"] == "user"
    assert round_2_messages[2]["role"] == "assistant"
    assert round_2_messages[3]["role"] == "tool"
    assert round_2_messages[3]["tool_call_id"] == "call_mock_12345"
