"""Script to run all online demos (00, 02, 03) and capture live screenshots S01, S03, S04, S07."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
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

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from report.capture_offline_screenshots import capture_and_render
from report.render_terminal_screenshot import SCREENSHOTS_DIR

SCRIPTS_DIR = REPO_ROOT / "draft" / "d02-3" / "scripts"


def main() -> None:
    print("Capturing S01: Demo 00 Minimal Triage...")
    capture_and_render(
        "Demo 00: Minimal Triage (Prose Output)",
        "00_minimal_triage.py",
        ["--issue", "API đăng nhập trả HTTP 503 cho toàn bộ người dùng từ 09:15."],
        "S01_demo00.png",
    )

    print("Capturing S03: Demo 02 Structured Output...")
    capture_and_render(
        "Demo 02: Structured Output & Invariant Validation",
        "02_structured_output.py",
        ["--runs", "3"],
        "S03_demo02.png",
    )

    print("Capturing S04: Demo 03 Function Calling...")
    capture_and_render(
        "Demo 03: Function Calling & 4-Stage Trace",
        "03_function_calling.py",
        [],
        "S04_demo03.png",
    )

    print("\nRe-compiling complete PDF report...")
    subprocess.run([sys.executable, str(REPO_ROOT / "report" / "build_report.py")], cwd=REPO_ROOT, check=True)
    subprocess.run([sys.executable, str(REPO_ROOT / "report" / "make_zip.py")], cwd=REPO_ROOT, check=True)
    print("\n🎉 Tất cả screenshot và bản PDF hoàn chỉnh đã được cập nhật thành công!")


if __name__ == "__main__":
    main()
