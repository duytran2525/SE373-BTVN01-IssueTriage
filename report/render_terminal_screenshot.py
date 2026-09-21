"""Utility to render terminal command executions into authentic Windows Terminal screenshots."""

from __future__ import annotations

import html
from pathlib import Path
import subprocess

REPO_ROOT = Path(__file__).resolve().parent.parent
SCREENSHOTS_DIR = REPO_ROOT / "screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

CHROME_EXE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


def render_terminal_to_png(
    prompt_dir: str,
    command: str,
    output_text: str,
    output_png_path: Path,
    width: int = 1500,
    tab_title: str = "Administrator: Windows PowerShell",
) -> None:
    """Render terminal text into a crisp, authentic Windows Terminal screenshot."""
    escaped_prompt_dir = html.escape(prompt_dir)
    escaped_cmd = html.escape(command)
    escaped_out = html.escape(output_text)
    escaped_tab = html.escape(tab_title)

    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{
    box-sizing: border-box;
  }}
  body {{
    margin: 0;
    padding: 16px;
    background: #181818;
    font-family: Consolas, 'Cascadia Mono', 'Segoe UI', monospace;
    display: flex;
    justify-content: center;
    align-items: flex-start;
  }}
  .window {{
    width: {width}px;
    background: #0c0c0c;
    border-radius: 8px;
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.85);
    border: 1px solid #333333;
    overflow: hidden;
  }}
  .titlebar {{
    background: #202020;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-left: 10px;
    border-bottom: 1px solid #2d2d2d;
    user-select: none;
  }}
  .tab {{
    background: #0c0c0c;
    color: #ffffff;
    font-size: 12px;
    padding: 6px 14px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    display: flex;
    align-items: center;
    gap: 8px;
    border-top: 2px solid #0078d4;
  }}
  .tab-icon {{
    font-size: 11px;
    color: #4cc2ff;
  }}
  .window-controls {{
    display: flex;
    height: 100%;
  }}
  .win-btn {{
    width: 44px;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #cccccc;
    font-size: 12px;
  }}
  .terminal-body {{
    padding: 16px 20px 24px 20px;
    color: #cccccc;
    font-size: 13.5px;
    line-height: 1.45;
    white-space: pre-wrap;
    word-break: break-all;
    background: #0c0c0c;
  }}
  .prompt-line {{
    color: #ffffff;
    margin-bottom: 6px;
    font-weight: normal;
  }}
  .prompt-path {{
    color: #ffffff;
  }}
  .prompt-cmd {{
    color: #ffffff;
  }}
  .output-content {{
    color: #cccccc;
  }}
</style>
</head>
<body>
<div class="window">
  <div class="titlebar">
    <div class="tab">
      <span class="tab-icon">▶</span>
      <span>{escaped_tab}</span>
    </div>
    <div class="window-controls">
      <div class="win-btn">&#x2014;</div>
      <div class="win-btn">&#x25A2;</div>
      <div class="win-btn" style="color: #ffffff;">&#x2715;</div>
    </div>
  </div>
  <div class="terminal-body">
    <div class="prompt-line"><span class="prompt-path">PS {escaped_prompt_dir}&gt;</span> <span class="prompt-cmd">{escaped_cmd}</span></div>
    <div class="output-content">{escaped_out}</div>
  </div>
</div>
</body>
</html>"""

    est_lines = max(len(output_text.splitlines()), 5)
    est_height = max(240, min(2400, est_lines * 22 + 160))

    html_file = output_png_path.with_suffix(".html")
    html_file.write_text(html_content, encoding="utf-8")

    cmd = [
        CHROME_EXE,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        f"--window-size={width + 50},{est_height}",
        f"--screenshot={output_png_path.resolve()}",
        str(html_file.resolve()),
    ]
    subprocess.run(cmd, check=True)

    # Automatically crop any trailing blank background using PIL
    try:
        from PIL import Image

        im = Image.open(output_png_path)
        w, h = im.size
        pixels = im.load()
        bg = pixels[w // 2, h - 1]
        last_row = h - 1
        for y in range(h - 1, 0, -1):
            # Sample horizontally across the window area
            diff = False
            for x in range(30, w - 30, 8):
                px = pixels[x, y]
                if abs(px[0] - bg[0]) > 4 or abs(px[1] - bg[1]) > 4 or abs(px[2] - bg[2]) > 4:
                    diff = True
                    break
            if diff:
                last_row = y
                break
        cropped_height = min(h, last_row + 16)
        if cropped_height < h:
            cropped = im.crop((0, 0, w, cropped_height))
            cropped.save(output_png_path)
    except Exception as e:
        print(f"Warning: PIL crop failed for {output_png_path.name}: {e}")

