import os
import zipfile
from pathlib import Path

ROOT = Path(r"C:\Users\Duy\SE373\BTVN02")
ZIP_PATH = ROOT / "BTVN1_IssueTriage_24520398.zip"

IGNORE_DIRS = {".venv", "venv", "__pycache__", ".pytest_cache", ".git", ".playwright-mcp", "tectonic_bin"}
IGNORE_FILES = {".env", "BTVN1_IssueTriage_24520398.zip"}

with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
        for f in filenames:
            if f in IGNORE_FILES or f.endswith(".pyc") or f.endswith(".tmp"):
                continue
            full_path = Path(dirpath) / f
            rel_path = full_path.relative_to(ROOT)
            zf.write(full_path, rel_path)

print(f"Zip created: {ZIP_PATH} ({ZIP_PATH.stat().st_size / 1024:.1f} KB)")
