"""Themes entity — list, install, delete themes."""
from typing import Any, Dict
from cli_anything.mautic.utils.api_client import MauticClient

def list_themes(client: MauticClient) -> Dict[str, Any]:
    """List themes: GET /api/themes."""
    return client.get_themes()

def install_theme(client: MauticClient, zip_path: str) -> Dict[str, Any]:
    """Install theme: POST /api/themes/new."""
    return client.install_theme(zip_path)

def delete_theme(client: MauticClient, theme_name: str) -> Dict[str, Any]:
    """Delete theme: DELETE /api/themes/{theme}/delete."""
    return client.delete_theme(theme_name)

def get_theme(client: MauticClient, theme_name: str) -> Dict[str, Any]:
    """Get theme zip: GET /api/themes/{theme}."""
    return client.get_theme(theme_name)
