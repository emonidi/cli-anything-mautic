"""Assets entity — CRUD operations."""

from typing import Any, Dict, List

from cli_anything.mautic.utils.api_client import MauticClient


def list_assets(client: MauticClient, **kwargs: Any) -> Dict[str, Any]:
    """List assets: GET /api/assets."""
    return client.list("assets", **kwargs)


def get_asset(client: MauticClient, asset_id: int) -> Dict[str, Any]:
    """Get asset: GET /api/assets/{id}."""
    return client.get("assets", asset_id)


def create_asset(client: MauticClient, data: Dict[str, Any]) -> Dict[str, Any]:
     """Create asset: POST /api/assets/new."""
    return client.create("assets", data)


def edit_asset(client: MauticClient, asset_id: int, data: Dict[str, Any],
               strict_mode: bool = False, ignore_missing: bool = False) -> Dict[str, Any]:
     """Edit asset: PATCH /api/assets/{id}/edit."""
    return client.edit("assets", asset_id, data, strict_mode, ignore_missing)


def update_asset(client: MauticClient, asset_id: int, data: Dict[str, Any],
                 strict_mode: bool = False, ignore_missing: bool = False) -> Dict[str, Any]:
     """Update asset: PUT /api/assets/{id}/edit."""
    return client.update("assets", asset_id, data, strict_mode, ignore_missing)


def delete_asset(client: MauticClient, asset_id: int) -> Dict[str, Any]:
     """Delete asset: DELETE /api/assets/{id}/delete."""
    return client.delete("assets", asset_id)


def batch_delete_assets(client: MauticClient, ids: List[int]) -> Dict[str, Any]:
     """Batch delete: POST /api/assets/batch/delete."""
    return client.batch_delete("assets", ids)


def batch_edit_assets(client: MauticClient, data: Dict[str, Any]) -> Dict[str, Any]:
     """Batch edit: PATCH /api/assets/batch/edit."""
    return client.batch_edit("assets", data)


def batch_update_assets(client: MauticClient, data: Dict[str, Any]) -> Dict[str, Any]:
     """Batch update: PUT /api/assets/batch/edit."""
    return client.batch_update("assets", data)


def batch_create_assets(client: MauticClient, items: List[Dict[str, Any]]) -> Dict[str, Any]:
     """Batch create: POST /api/assets/batch/new."""
    return client.batch_create("assets", items)
