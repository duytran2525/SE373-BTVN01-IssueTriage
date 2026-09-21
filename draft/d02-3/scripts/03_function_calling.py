#!/usr/bin/env python3
"""Demo 03: Application-controlled tool execution with 4-stage trace (R5, R6)."""

from __future__ import annotations

import argparse
import json
import sys

from demo_common import model_name, openai_client
from triage_workflow import COMPONENT_OWNERS, execute_tool_call, triage_issue

DEFAULT_ISSUE = (
    "Nút thanh toán trả HTTP 500 với mọi thẻ Visa từ 14:30. "
    "Hãy triage issue và cho biết team nào cần xử lý."
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--issue", default=DEFAULT_ISSUE, help="Nội dung issue cần triage.")
    parser.add_argument(
        "--show-messages",
        action="store_true",
        help="In chi tiết danh sách messages gửi và nhận trong quá trình agent loop.",
    )
    parser.add_argument(
        "--simulate-bad-call",
        metavar="COMPONENT",
        help="Giả lập một lời gọi tool với component không hợp lệ (ví dụ: billing) để minh họa cơ chế phòng thủ của application.",
    )
    args = parser.parse_args()

    print("=== DEMO 03: FUNCTION CALLING & 4-STAGE TRACE (R5, R6) ===")
    print("Mô hình: Model đề xuất (propose) -> Application kiểm soát và thực thi (execute)")
    print("-" * 75)

    # Simulation mode (offline test of security boundary)
    if args.simulate_bad_call:
        print(f"\n[SIMULATED] Thử nghiệm tiêm tool proposal không hợp lệ: component={args.simulate_bad_call!r}")
        print("1. Giả lập Model gửi tool call:")
        raw_args = json.dumps({"component": args.simulate_bad_call})
        print(f"   get_component_owner(component={args.simulate_bad_call!r})")
        print("\n2. Application thẩm tra và thực thi (Treating model as untrusted input):")
        result = execute_tool_call("get_component_owner", raw_args)
        print(f"   Kết quả từ Application: {json.dumps(result, ensure_ascii=False, indent=2)}")
        print("\n=> Cơ chế bảo mật: Application chặn thành công lời gọi bất hợp pháp mà không làm sập tiến trình.")
        return

    try:
        client = openai_client()
        model = model_name()
    except Exception as config_err:
        print(f"[CẤU HÌNH LỖI] Không thể khởi tạo API client: {config_err}", file=sys.stderr)
        sys.exit(1)

    print(f"Issue: {args.issue}")
    print("=" * 75)

    try:
        result = triage_issue(client, model, args.issue)
    except Exception as err:
        print(f"[API ERROR] Lỗi trong quá trình chạy triage tool loop: {err}", file=sys.stderr)
        sys.exit(1)

    # Print strict 4-stage trace
    for idx, trace in enumerate(result.tool_traces, start=1):
        print(f"\n=== 1. Model đề xuất tool call (Stage 1: tool_call #{idx}) ===")
        print(
            json.dumps(
                {
                    "call_id": trace.call_id,
                    "tool_name": trace.name,
                    "arguments": trace.arguments,
                },
                ensure_ascii=False,
                indent=2,
            )
        )

        comp = trace.arguments.get("component", "unknown")
        owner = trace.result.get("owner", "N/A")
        print(f"\n=== 2. Application thực thi (Stage 2: application executes) ===")
        print(f"   [Thẩm định allowlist: '{comp}' in {list(COMPONENT_OWNERS.keys())}] -> Hợp lệ ✔")
        print(f"   get_component_owner({comp!r}) -> {owner!r}")

        print(f"\n=== 3. Tool result quay lại model (Stage 3: tool_result) ===")
        print(json.dumps(trace.result, ensure_ascii=False, indent=2))

    print("\n=== 4. Final response từ model (Stage 4: final response) ===")
    print(result.final_response)
    print("=" * 75)

    if args.show_messages:
        print("\n[CHI TIẾT CONVERSATION MESSAGES]:")
        for i, m in enumerate(result.messages):
            if hasattr(m, "role"):
                role = m.role
                content = m.content
                tool_calls = m.tool_calls
                tool_call_id = getattr(m, "tool_call_id", None)
            else:
                role = m.get("role", "")
                content = m.get("content")
                tool_calls = m.get("tool_calls")
                tool_call_id = m.get("tool_call_id")

            print(f"\n--- Message [{i}] (Role: {role}) ---")
            if content:
                print(f"Content: {content}")
            if tool_calls:
                tc_repr = [
                    {"id": tc.id, "name": tc.function.name, "arguments": tc.function.arguments}
                    if hasattr(tc, "function") else tc
                    for tc in tool_calls
                ]
                print(f"Tool Calls: {json.dumps(tc_repr, ensure_ascii=False)}")
            if tool_call_id:
                print(f"Tool Call ID: {tool_call_id}")


if __name__ == "__main__":
    main()
