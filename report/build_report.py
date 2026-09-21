#!/usr/bin/env python3
"""Automated report generation script: outputs real data and screenshots into a PDF report (S3)."""

from __future__ import annotations

import argparse
import base64
import csv
import datetime
import os
from pathlib import Path
import subprocess
import sys

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

REPORT_DIR = Path(__file__).resolve().parent
REPO_ROOT = REPORT_DIR.parent
OUTPUTS_DIR = REPO_ROOT / "outputs"
SCREENSHOTS_DIR = REPO_ROOT / "screenshots"

DEFAULT_STUDENT_NAME = "Trần Đình Duy"
DEFAULT_STUDENT_ID = "24520398"
DEFAULT_CLASS_NAME = "SE373.R11"


def find_browser_executable() -> str | None:
    """Find Chrome or Edge executable on the host machine."""
    candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium-browser",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    ]
    for c in candidates:
        if Path(c).exists():
            return c
    return None


def image_to_base64_tag(img_path: Path, alt_text: str) -> str:
    """Convert an image file to an inline base64 HTML img tag."""
    if not img_path.exists():
        return (
            f'<div style="border: 2px dashed #94a3b8; padding: 24px; text-align: center; '
            f'background: #f8fafc; border-radius: 6px; color: #64748b;">'
            f'📷 <strong>[Chưa có ảnh chụp {img_path.name}]</strong><br>'
            f'<span style="font-size: 8.5pt;">Vui lòng lưu ảnh chụp màn hình vào <code>screenshots/{img_path.name}</code></span>'
            f'</div>'
        )
    with open(img_path, "rb") as f:
        data = base64.b64encode(f.read()).decode("ascii")
    ext = img_path.suffix.lower().replace(".", "")
    mime = "image/png" if ext == "png" else "image/jpeg"
    return f'<img src="data:{mime};base64,{data}" alt="{alt_text}" style="max-width: 100%; height: auto; border: 1px solid #cbd5e1; border-radius: 4px;" />'


def build_tokens_table_html() -> str:
    """Generate HTML table from outputs/01_tokens.csv."""
    csv_path = OUTPUTS_DIR / "01_tokens.csv"
    if not csv_path.exists():
        csv_path = REPO_ROOT / "draft" / "d02-3" / "outputs" / "01_tokens.csv"
    if not csv_path.exists():
        return "<p><em>(Chưa có file outputs/01_tokens.csv. Hãy chạy 01_measure_tokens.py trước).</em></p>"

    rows = []
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)

    html = [
        "<table>",
        "<thead><tr>",
        "<th>ID</th><th>Thể loại ngữ liệu</th><th>Ngôn ngữ</th><th>Ký tự</th><th>Bytes UTF-8</th>",
        "<th>cl100k</th><th>o200k</th><th>Tỉ lệ VI/EN (cl100k)</th><th>Tỉ lệ VI/EN (o200k)</th>",
        "</tr></thead><tbody>",
    ]

    for r in rows:
        lang_badge = f'<span class="badge badge-{"blue" if r["lang"] == "EN" else "green"}">{r["lang"]}</span>'
        html.append(
            f"<tr>"
            f"<td>{r['id']}</td>"
            f"<td>{r['category']}</td>"
            f"<td>{lang_badge}</td>"
            f"<td>{r['chars']}</td>"
            f"<td>{r['bytes']}</td>"
            f"<td><strong>{r['tokens_cl100k']}</strong></td>"
            f"<td><strong>{r['tokens_o200k']}</strong></td>"
            f"<td>{r['vi_en_ratio_cl100k']}</td>"
            f"<td>{r['vi_en_ratio_o200k']}</td>"
            f"</tr>"
        )

    html.append("</tbody></table>")
    return "\n".join(html)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--drive-link",
        default="https://drive.google.com/drive/folders/1VnC2U7_6K6I3osFo8Xwh94QjENsGtCFi?usp=sharing",
        help="Liên kết Google Drive chứa source code (share Anyone with the link - Viewer).",
    )
    parser.add_argument(
        "--github-link",
        default="https://github.com/duytran2525/SE373-BTVN01-IssueTriage",
        help="Liên kết GitHub Repository public.",
    )
    parser.add_argument("--name", default=DEFAULT_STUDENT_NAME, help="Họ và tên sinh viên.")
    parser.add_argument("--id", default=DEFAULT_STUDENT_ID, help="Mã số sinh viên.")
    parser.add_argument("--class-name", default=DEFAULT_CLASS_NAME, help="Tên lớp.")
    args = parser.parse_args()

    template_file = REPORT_DIR / "report_template.html"
    if not template_file.exists():
        print(f"Lỗi: Không tìm thấy file template tại {template_file}", file=sys.stderr)
        sys.exit(1)

    template_content = template_file.read_text(encoding="utf-8")

    # Replace student metadata
    now_str = datetime.date.today().strftime("%d/%m/%Y")
    filled = template_content.replace("{{STUDENT_NAME}}", args.name)
    filled = filled.replace("{{STUDENT_ID}}", args.id)
    filled = filled.replace("{{CLASS_NAME}}", args.class_name)
    filled = filled.replace("{{SUBMISSION_DATE}}", now_str)
    filled = filled.replace("{{DRIVE_LINK}}", args.drive_link)
    filled = filled.replace("{{GITHUB_LINK}}", args.github_link)

    # Replace real tokens data table
    table_html = build_tokens_table_html()
    filled = filled.replace("{{TABLE_TOKENS_01}}", table_html)

    # Embed Screenshots
    s01_tag = image_to_base64_tag(SCREENSHOTS_DIR / "S01_demo00.png", "Demo 00 output")
    s02_tag = image_to_base64_tag(SCREENSHOTS_DIR / "S02_demo01.png", "Demo 01 Token Measurement")
    s03_tag = image_to_base64_tag(SCREENSHOTS_DIR / "S03_demo02.png", "Demo 02 output")
    s04_tag = image_to_base64_tag(SCREENSHOTS_DIR / "S04_demo03.png", "Demo 03 output")
    s05_tag = image_to_base64_tag(SCREENSHOTS_DIR / "S05_demo04_terminal.png", "Demo 04 Streamlit Terminal")
    s06_tag = image_to_base64_tag(SCREENSHOTS_DIR / "S06_demo04_ui_input.png", "Demo 04 UI input")
    s07_tag = image_to_base64_tag(SCREENSHOTS_DIR / "S07_demo04_ui_result.png", "Demo 04 UI result")
    s08_tag = image_to_base64_tag(SCREENSHOTS_DIR / "S08_pytest.png", "Pytest Suite Results")

    filled = filled.replace("{{SCREENSHOT_S01}}", s01_tag)
    filled = filled.replace("{{SCREENSHOT_S02}}", s02_tag)
    filled = filled.replace("{{SCREENSHOT_S03}}", s03_tag)
    filled = filled.replace("{{SCREENSHOT_S04}}", s04_tag)
    filled = filled.replace("{{SCREENSHOT_S05}}", s05_tag)
    filled = filled.replace("{{SCREENSHOT_S06}}", s06_tag)
    filled = filled.replace("{{SCREENSHOT_S07}}", s07_tag)
    filled = filled.replace("{{SCREENSHOT_S08}}", s08_tag)

    rendered_html_path = REPORT_DIR / "report_filled.html"
    rendered_html_path.write_text(filled, encoding="utf-8")
    print(f"Đã xuất bản HTML trung gian tại: {rendered_html_path}")

    # Build PDF using headless browser
    browser_exe = find_browser_executable()
    pdf_output_path = REPO_ROOT / f"BTVN1_IssueTriage_{args.id}.pdf"

    if not browser_exe:
        print("Không tìm thấy Chrome hoặc Edge để xuất PDF trực tiếp. Giữ file HTML để xem hoặc in bằng tay.")
        return

    print(f"Đang xuất PDF bằng trình duyệt headless: {browser_exe}...")
    cmd = [
        browser_exe,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_output_path.resolve()}",
        str(rendered_html_path.resolve()),
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"🎉 XUẤT BÁO CÁO PDF THÀNH CÔNG: {pdf_output_path}")
        print(f"   Kích thước file PDF: {pdf_output_path.stat().st_size / 1024:.1f} KB")
    except Exception as err:
        print(f"Lỗi khi gọi trình duyệt xuất PDF: {err}", file=sys.stderr)


if __name__ == "__main__":
    main()
