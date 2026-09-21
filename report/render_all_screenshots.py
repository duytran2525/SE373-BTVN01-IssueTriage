#!/usr/bin/env python3
"""Script to generate all screenshots from verified outputs in outputs/."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = ROOT / "outputs"
SCREENSHOTS_DIR = ROOT / "screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from report.render_terminal_screenshot import render_terminal_to_png

SCRIPTS_DIR_PROMPT = r"C:\Users\Duy\SE373\BTVN02\draft\d02-3\scripts"
ROOT_DIR_PROMPT = r"C:\Users\Duy\SE373\BTVN02"


def main() -> None:
    # S01: Demo 00
    txt_00 = (OUTPUTS_DIR / "00_minimal_triage.txt").read_text(encoding="utf-8")
    render_terminal_to_png(
        SCRIPTS_DIR_PROMPT,
        'python 00_minimal_triage.py --issue "API đăng nhập trả HTTP 503 cho toàn bộ người dùng từ 09:15."',
        txt_00,
        SCREENSHOTS_DIR / "S01_demo00.png",
    )
    print("Rendered S01_demo00.png")

    # S02a & S02b: Demo 01
    txt_01 = (OUTPUTS_DIR / "01_measure_tokens.txt").read_text(encoding="utf-8")
    split_marker = "=== MINH HỌA PHÂN MẢNH TOKEN (TOKEN FRAGMENTATION) TIẾNG VIỆT ==="
    if split_marker in txt_01:
        part_a, part_b = txt_01.split(split_marker, 1)
        part_b = split_marker + "\n" + part_b
    else:
        part_a, part_b = txt_01, txt_01

    render_terminal_to_png(
        SCRIPTS_DIR_PROMPT,
        "python 01_measure_tokens.py",
        part_a.strip(),
        SCREENSHOTS_DIR / "S02a_demo01_table.png",
    )
    render_terminal_to_png(
        SCRIPTS_DIR_PROMPT,
        "python 01_measure_tokens.py  [Phần phân mảnh byte UTF-8]",
        part_b.strip(),
        SCREENSHOTS_DIR / "S02b_demo01_bytes.png",
    )
    print("Rendered S02a_demo01_table.png and S02b_demo01_bytes.png")

    # S03a & S03b: Demo 02
    txt_02 = (OUTPUTS_DIR / "02_structured_output.txt").read_text(encoding="utf-8")
    split_02_marker = "[PHẦN B] STRUCTURED OUTPUT"
    if split_02_marker in txt_02:
        p02_a, p02_b = txt_02.split(split_02_marker, 1)
        p02_b = split_02_marker + p02_b
    else:
        p02_a, p02_b = txt_02, txt_02

    render_terminal_to_png(
        SCRIPTS_DIR_PROMPT,
        "python 02_structured_output.py --runs 10",
        p02_a.strip(),
        SCREENSHOTS_DIR / "S03a_demo02_A.png",
    )
    render_terminal_to_png(
        SCRIPTS_DIR_PROMPT,
        "python 02_structured_output.py --runs 10  [Phần B & C]",
        p02_b.strip(),
        SCREENSHOTS_DIR / "S03b_demo02_B_C.png",
    )
    print("Rendered S03a_demo02_A.png and S03b_demo02_B_C.png")

    # S04a: Demo 03 Default
    txt_03 = (OUTPUTS_DIR / "03_function_calling.txt").read_text(encoding="utf-8")
    render_terminal_to_png(
        SCRIPTS_DIR_PROMPT,
        "python 03_function_calling.py",
        txt_03.strip(),
        SCREENSHOTS_DIR / "S04a_demo03.png",
    )
    print("Rendered S04a_demo03.png")

    # S04b: Demo 03 Messages
    txt_03_msgs = (OUTPUTS_DIR / "03_show_messages.txt").read_text(encoding="utf-8")
    render_terminal_to_png(
        SCRIPTS_DIR_PROMPT,
        "python 03_function_calling.py --show-messages",
        txt_03_msgs.strip(),
        SCREENSHOTS_DIR / "S04b_demo03_messages.png",
    )
    print("Rendered S04b_demo03_messages.png")

    # S05: Streamlit Terminal startup
    st_log = """2026-09-21 19:27:32.063 Uvicorn server started on :::8501

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://172.16.0.2:8501
  External URL: http://***.***.***.***:8501  [IP công khai đã được che giấu an toàn]"""
    render_terminal_to_png(
        SCRIPTS_DIR_PROMPT,
        "streamlit run 04_streamlit_triage.py --server.headless true",
        st_log,
        SCREENSHOTS_DIR / "S05_demo04_terminal.png",
    )
    print("Rendered S05_demo04_terminal.png")

    # S08: Pytest
    txt_pytest = (OUTPUTS_DIR / "pytest.txt").read_text(encoding="utf-8")
    render_terminal_to_png(
        ROOT_DIR_PROMPT,
        "pytest -v",
        txt_pytest.strip(),
        SCREENSHOTS_DIR / "S08_pytest.png",
    )
    print("Rendered S08_pytest.png")

    # S10: Adversarial
    txt_adv = (OUTPUTS_DIR / "02_adversarial.txt").read_text(encoding="utf-8")
    render_terminal_to_png(
        SCRIPTS_DIR_PROMPT,
        "python 02_structured_output.py --adversarial",
        txt_adv.strip(),
        SCREENSHOTS_DIR / "S10_adversarial.png",
    )
    print("Rendered S10_adversarial.png")

    # S11: Simulate Bad Call
    txt_bad = (OUTPUTS_DIR / "03_simulate_bad_call.txt").read_text(encoding="utf-8")
    render_terminal_to_png(
        SCRIPTS_DIR_PROMPT,
        "python 03_function_calling.py --simulate-bad-call billing",
        txt_bad.strip(),
        SCREENSHOTS_DIR / "S11_simulate_bad_call.png",
    )
    print("Rendered S11_simulate_bad_call.png")


if __name__ == "__main__":
    main()
