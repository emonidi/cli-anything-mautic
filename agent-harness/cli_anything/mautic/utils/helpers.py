"""Helper functions for creating MauticClient from project config."""

import os
from typing import Any, Dict, Optional

from cli_anything.mautic.core.project import load_project
from cli_anything.mautic.utils.api_client import MauticClient


def get_client(project_path: Optional[str] = None) -> MauticClient:
    """Create a MauticClient from the project config.

    Raises RuntimeError if base_url is not configured.
    """
    proj = load_project(project_path)
    base_url = proj.get("base_url", "")
    if not base_url:
        raise RuntimeError(
            "No Mautic instance configured. "
            "Run: cli-anything-mautic config set --base-url <url>"
        )
    return MauticClient(
        base_url=base_url,
        api_key_id=proj.get("api_key_id", ""),
        api_key_secret=proj.get("api_key_secret", ""),
        oauth2_token_endpoint=proj.get("oauth2_token_endpoint", ""),
        api_version=proj.get("api_version", "2"),
    )


def get_project(project_path: Optional[str] = None) -> Dict[str, Any]:
    """Load and return project config."""
    return load_project(project_path)


def ensure_client(project_path: Optional[str] = None) -> MauticClient:
    """Alias for get_client."""
    return get_client(project_path)
