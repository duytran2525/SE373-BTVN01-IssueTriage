#!/usr/bin/env python3
"""Linter script to enforce strict academic and verification quality gates before PDF publishing (Phase G)."""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

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

ROOT = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = ROOT / "outputs"
SCREENSHOTS_DIR = ROOT / "screenshots"
REPORT_DIR = ROOT / "report"

FORBIDDEN_WORDS = [
    "xuất sắc",
    "hoàn hảo",
    "mọi nhà cung cấp",
    "commit history hoàn chỉnh",
    "TODO",
    "[CHƯA CÓ ẢNH]",
]


def lint_report() -> bool:
    print("=== CHẠY REPORT_LINT (QUALITY ASSURANCE GATE) ===")
    errors = []

    # 1. Check outputs files exist
    required_outputs = [
        "00_minimal_triage.txt",
        "01_measure_tokens.txt",
        "01_tokens.csv",
        "02_structured_output.txt",
        "02_results.csv",
        "02_adversarial.txt",
        "03_function_calling.txt",
        "03_show_messages.txt",
        "03_simulate_bad_call.txt",
        "pytest.txt",
        "run_meta.json",
    ]
    for ro in required_outputs:
        p = OUTPUTS_DIR / ro
        if not p.exists() or p.stat().st_size == 0:
            errors.append(f"Tệp đầu ra thiếu hoặc rỗng: outputs/{ro}")
        else:
            print(f"✔ Tệp đầu ra tồn tại: outputs/{ro} ({p.stat().st_size} bytes)")

    # 2. Check pytest 19 passed and unique
    pytest_txt = (OUTPUTS_DIR / "pytest.txt").read_text(encoding="utf-8")
    passed_lines = [l for l in pytest_txt.splitlines() if "PASSED" in l]
    if len(passed_lines) != 19:
        errors.append(f"Số lượng passed test cases ({len(passed_lines)}) không khớp 19.")
    else:
        print("✔ Pytest: Chính xác 19 test cases PASSED.")
    if len(passed_lines) != len(set(passed_lines)):
        errors.append("Pytest có dòng kết quả bị trùng lặp!")
    else:
        print("✔ Pytest: Không có dòng kết quả nào bị trùng lặp.")

    # 3. Check model ID consistency
    meta = json.loads((OUTPUTS_DIR / "run_meta.json").read_text(encoding="utf-8"))
    canonical_model = meta["openai_model"]
    print(f"✔ Canonical Model ID từ run_meta.json: {canonical_model}")
    for txt_file in ["00_minimal_triage.txt", "02_structured_output.txt", "03_function_calling.txt"]:
        content = (OUTPUTS_DIR / txt_file).read_text(encoding="utf-8")
        if canonical_model not in content and "gemini" in content.lower():
            errors.append(f"Model ID trong outputs/{txt_file} không khớp {canonical_model}.")

    # 4. Check report template has no forbidden words
    template_text = (REPORT_DIR / "report_template.html").read_text(encoding="utf-8")
    for fw in FORBIDDEN_WORDS:
        if fw in template_text:
            errors.append(f"Báo cáo chứa cụm từ bị cấm: '{fw}'")
        else:
            print(f"✔ Không chứa cụm từ bị cấm: '{fw}'")

    # 5. Check all referenced screenshots exist
    img_matches = re.findall(r"S\d+[a-z_]*\.png", template_text)
    for img_name in set(img_matches):
        img_p = SCREENSHOTS_DIR / img_name
        if not img_p.exists():
            errors.append(f"Ảnh được trỏ tới không tồn tại trong screenshots/: {img_name}")
        else:
            print(f"✔ Ảnh tồn tại: screenshots/{img_name} ({img_p.stat().st_size} bytes)")

    # 6. Check report has Section S1 and Provenance table
    if "Đối chiếu với Demo gốc của Giảng viên" not in template_text:
        errors.append("Thiếu mục đối chiếu với demo gốc (S1).")
    else:
        print("✔ Mục đối chiếu với demo gốc (S1) hiện diện.")

    if "Bảng Nguồn gốc" not in template_text and "Provenance Table" not in template_text:
        errors.append("Thiếu bảng Provenance (Phụ lục C).")
    else:
        print("✔ Bảng Provenance (Phụ lục C) hiện diện.")

    # Summary
    if errors:
        print("\n❌ PHÁT HIỆN LỖI LINT BÁO CÁO:")
        for e in errors:
            print(f"  - {e}")
        return False

    print("\n🎉 TOÀN BỘ TIÊU CHÍ QA CỦA BÁO CÁO ĐÃ ĐẠT 100%!")
    return True


if __name__ == "__main__":
    success = lint_report()
    if not success:
        sys.exit(1)
