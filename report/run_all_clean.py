#!/usr/bin/env python3
"""Clean execution runner to capture real command outputs directly in UTF-8 without Windows pipe mojibake."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

SCRIPTS_DIR = ROOT / "draft" / "d02-3" / "scripts"
OUTPUTS_DIR = ROOT / "outputs"
DRAFT_OUTPUTS_DIR = ROOT / "draft" / "d02-3" / "outputs"

OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
DRAFT_OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

COMMANDS = [
    (
        "00_minimal_triage",
        [sys.executable, "00_minimal_triage.py", "--issue", "API đăng nhập trả HTTP 503 cho toàn bộ người dùng từ 09:15."],
        SCRIPTS_DIR,
    ),
    (
        "01_measure_tokens",
        [sys.executable, "01_measure_tokens.py"],
        SCRIPTS_DIR,
    ),
    (
        "02_structured_output",
        [sys.executable, "02_structured_output.py", "--runs", "10"],
        SCRIPTS_DIR,
    ),
    (
        "02_adversarial",
        [sys.executable, "02_structured_output.py", "--adversarial"],
        SCRIPTS_DIR,
    ),
    (
        "03_function_calling",
        [sys.executable, "03_function_calling.py"],
        SCRIPTS_DIR,
    ),
    (
        "03_show_messages",
        [sys.executable, "03_function_calling.py", "--show-messages"],
        SCRIPTS_DIR,
    ),
    (
        "03_simulate_bad_call",
        [sys.executable, "03_function_calling.py", "--simulate-bad-call", "billing"],
        SCRIPTS_DIR,
    ),
    (
        "pytest",
        ["pytest", "-v"],
        ROOT,
    ),
]


def main() -> None:
    for name, cmd, cwd in COMMANDS:
        print(f"\n=======================================================")
        print(f"Executing: {' '.join(cmd)} in {cwd}")
        print(f"=======================================================")
        res = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        combined = res.stdout
        if res.stderr:
            combined += ("\n[STDERR]\n" + res.stderr)

        print(combined[:300] + ("..." if len(combined) > 300 else ""))

        p1 = OUTPUTS_DIR / f"{name}.txt"
        p2 = DRAFT_OUTPUTS_DIR / f"{name}.txt"
        p1.write_text(combined, encoding="utf-8")
        p2.write_text(combined, encoding="utf-8")
        print(f"-> Saved: {p1}")


if __name__ == "__main__":
    main()
