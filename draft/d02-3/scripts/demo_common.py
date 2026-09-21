"""Shared configuration and utilities for the Buổi 02 executable demos."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

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

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
REPOSITORY_ROOT = SCRIPT_DIRECTORY.parents[2]


def mask_secret(value: str | None) -> str:
    """Safely mask secret strings such as API keys for logging and display."""
    if not value:
        return "[NOT SET]"
    val = value.strip()
    if len(val) <= 8:
        return "****"
    return f"{val[:4]}...{val[-4:]}"


def load_environment() -> None:
    """Load script-directory .env first, then repository-root .env."""
    if (SCRIPT_DIRECTORY / ".env").exists():
        load_dotenv(SCRIPT_DIRECTORY / ".env")
    if (REPOSITORY_ROOT / ".env").exists():
        load_dotenv(REPOSITORY_ROOT / ".env")


def model_name() -> str:
    """Return the configured model ID."""
    load_environment()
    model = os.getenv("OPENAI_MODEL")
    if not model:
        raise RuntimeError(
            "OPENAI_MODEL is required. Set a valid model ID in .env (e.g., gemini-1.5-flash or gpt-4o-mini)."
        )
    return model.strip()


def api_base_url() -> str:
    """Return the configured base URL."""
    load_environment()
    base_url = os.getenv("OPENAI_BASE_URL")
    if not base_url:
        raise RuntimeError(
            "OPENAI_BASE_URL is required. Set the OpenAI-compatible base URL in .env."
        )
    return base_url.strip()


def openai_client(timeout: float = 60.0, max_retries: int = 2) -> OpenAI:
    """Create a client for the configured OpenAI-compatible API endpoint."""
    load_environment()
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = api_base_url()
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is required. Copy .env.example to .env and set a valid API key."
        )
    return OpenAI(
        api_key=api_key.strip(),
        base_url=base_url,
        timeout=timeout,
        max_retries=max_retries,
    )
