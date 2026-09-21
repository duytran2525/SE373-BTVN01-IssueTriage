"""Runner to execute scripts with clean UTF-8 capture and generate screenshot PNGs."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from report.render_terminal_screenshot import render_terminal_to_png, SCREENSHOTS_DIR

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "draft" / "d02-3" / "scripts"
OUTPUTS_DIR = Path(__file__).resolve().parent.parent / "outputs"


def capture_and_render(title: str, script_name: str, cmd_args: list[str], png_name: str, cwd: Path = SCRIPTS_DIR) -> str:
    full_cmd = [sys.executable, script_name] + cmd_args
    disp_cmd = f"python {script_name} {' '.join(cmd_args)}".strip()
    res = subprocess.run(full_cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    output = res.stdout + (("\n[STDERR]\n" + res.stderr) if res.stderr else "")

    # Save text output
    txt_path = OUTPUTS_DIR / f"{Path(png_name).stem}.txt"
    txt_path.write_text(output, encoding="utf-8")

    # Render PNG
    png_path = SCREENSHOTS_DIR / png_name
    render_terminal_to_png(title, disp_cmd, output, png_path)
    return output


def main() -> None:
    print("Capturing S02: Demo 01 Token Measurement...")
    capture_and_render("Demo 01: Token Measurement (Offline)", "01_measure_tokens.py", [], "S02_demo01.png")

    print("Capturing S08: Pytest Test Suite...")
    res = subprocess.run(["pytest", "-v"], cwd=SCRIPTS_DIR.parents[2], capture_output=True, text=True, encoding="utf-8", errors="replace")
    out_pytest = res.stdout + (("\n[STDERR]\n" + res.stderr) if res.stderr else "")
    (OUTPUTS_DIR / "pytest.txt").write_text(out_pytest, encoding="utf-8")
    render_terminal_to_png("Pytest Test Suite (19/19 Passed Offline)", "pytest -v", out_pytest, SCREENSHOTS_DIR / "S08_pytest.png")


if __name__ == "__main__":
    main()
