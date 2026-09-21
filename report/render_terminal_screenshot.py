"""Utility to render terminal command executions into crisp, high-resolution terminal screenshot PNGs."""

from __future__ import annotations

from pathlib import Path
import subprocess

REPO_ROOT = Path(__file__).resolve().parent.parent
SCREENSHOTS_DIR = REPO_ROOT / "screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

CHROME_EXE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


def render_terminal_to_png(title: str, command: str, output_text: str, output_png_path: Path, width: int = 1400) -> None:
    """Render terminal text into a professional terminal mockup and screenshot with headless Chrome."""
    import html

    escaped_title = html.escape(title)
    escaped_cmd = html.escape(command)
    escaped_out = html.escape(output_text)

    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{
    margin: 0;
    padding: 30px;
    background: #0f172a;
    font-family: 'JetBrains Mono', 'Consolas', monospace;
    display: flex;
    justify-content: center;
    align-items: flex-start;
  }}
  .window {{
    width: {width - 60}px;
    background: #181825;
    border-radius: 12px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
    border: 1px solid #313244;
    overflow: hidden;
  }}
  .titlebar {{
    background: #11111b;
    padding: 12px 18px;
    display: flex;
    align-items: center;
    border-bottom: 1px solid #313244;
  }}
  .buttons {{
    display: flex;
    gap: 8px;
  }}
  .btn {{
    width: 13px;
    height: 13px;
    border-radius: 50%;
  }}
  .btn-red {{ background: #f38ba8; }}
  .btn-yellow {{ background: #f9e2af; }}
  .btn-green {{ background: #a6e3a1; }}
  .title {{
    flex: 1;
    text-align: center;
    color: #a6adc8;
    font-size: 13px;
    font-weight: 600;
  }}
  .terminal-body {{
    padding: 22px 26px;
    color: #cdd6f4;
    font-size: 14px;
    line-height: 1.6;
    white-space: pre-wrap;
    word-break: break-word;
  }}
  .prompt-line {{
    color: #89b4fa;
    margin-bottom: 12px;
    font-weight: 600;
  }}
  .prompt-symbol {{
    color: #a6e3a1;
  }}
</style>
</head>
<body>
<div class="window">
  <div class="titlebar">
    <div class="buttons">
      <div class="btn btn-red"></div>
      <div class="btn btn-yellow"></div>
      <div class="btn btn-green"></div>
    </div>
    <div class="title">{escaped_title}</div>
  </div>
  <div class="terminal-body">
    <div class="prompt-line"><span class="prompt-symbol">duy@uit-agentic:~/BTVN02/draft/d02-3/scripts$</span> {escaped_cmd}</div>
{escaped_out}
  </div>
</div>
</body>
</html>"""

    temp_html = output_png_path.parent / f"{output_png_path.stem}.html"
    temp_html.write_text(html_content, encoding="utf-8")

    # Run Chrome screenshot
    cmd = [
        CHROME_EXE,
        "--headless",
        "--disable-gpu",
        f"--window-size={width},1100",
        f"--screenshot={output_png_path.resolve()}",
        str(temp_html.resolve()),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"Captured screenshot: {output_png_path} ({output_png_path.stat().st_size / 1024:.1f} KB)")
