#!/usr/bin/env python3
"""Demo 00: Minimal LLM triage call producing free-form prose output (R1, R2)."""

from __future__ import annotations

import argparse
import sys
import time

from demo_common import mask_secret, model_name, openai_client
from prompts import build_messages

DEFAULT_ISSUE = "API đăng nhập trả HTTP 503 cho toàn bộ người dùng từ 09:15."


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--issue",
        default=DEFAULT_ISSUE,
        help="Nội dung mô tả issue cần phân loại.",
    )
    args = parser.parse_args()

    try:
        client = openai_client()
        model = model_name()
    except Exception as err:
        print(f"[CẤU HÌNH LỖI] {err}", file=sys.stderr)
        sys.exit(1)

    messages = build_messages(args.issue)

    print("=== DEMO 00: LLM TRIAGE TỐI THIỂU (PROSE OUTPUT) ===")
    print(f"Model ID : {model}")
    print(f"Issue    : {args.issue}")
    print("-" * 60)

    start_time = time.perf_counter()
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.2,
        )
    except Exception as err:
        print(f"[API ERROR] Gọi LLM thất bại: {err}", file=sys.stderr)
        sys.exit(1)

    latency = time.perf_counter() - start_time
    choice = response.choices[0]
    content = choice.message.content or ""
    usage = response.usage

    print(f"Độ trễ phản hồi : {latency:.2f} giây")
    if usage:
        print(
            f"Token Usage     : prompt={usage.prompt_tokens}, "
            f"completion={usage.completion_tokens}, total={usage.total_tokens}"
        )
    print("-" * 60)
    print("KẾT QUẢ TRIAGE (VĂN BẢN TỰ DO):")
    print(content)


if __name__ == "__main__":
    main()
