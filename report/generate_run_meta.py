import json
import sys
import platform
import subprocess
import datetime
import os
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(r"C:\Users\Duy\SE373\BTVN02")
env_path = ROOT / "draft" / "d02-3" / "scripts" / ".env"

env_vars = {}
if env_path.exists():
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env_vars[k.strip()] = v.strip().strip("\"'")

base_url = env_vars.get("OPENAI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")
parsed_url = urlparse(base_url)
host = f"{parsed_url.scheme}://{parsed_url.netloc}"
model = env_vars.get("OPENAI_MODEL", "gemini-3.6-flash")

pip_freeze_res = subprocess.run([sys.executable, "-m", "pip", "freeze"], capture_output=True, text=True, encoding="utf-8", errors="ignore")
pip_freeze = pip_freeze_res.stdout.strip().splitlines()

git_sha_res = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="ignore")
git_sha = git_sha_res.stdout.strip()

meta = {
    "os": platform.platform(),
    "system": platform.system(),
    "release": platform.release(),
    "machine": platform.machine(),
    "python_version": sys.version,
    "shell": "Windows PowerShell 5.1 / pwsh",
    "openai_model": model,
    "base_url_host": host,
    "git_sha": git_sha,
    "timestamp_iso": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "pip_freeze": pip_freeze,
}

out_path = ROOT / "outputs" / "run_meta.json"
out_path.parent.mkdir(parents=True, exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(meta, f, indent=2, ensure_ascii=False)

print(f"Generated {out_path} successfully.")
print(f"OS: {meta['os']}")
print(f"Python: {meta['python_version'].split()[0]}")
print(f"Model: {model}")
print(f"Host: {host}")
print(f"Git SHA: {git_sha}")
