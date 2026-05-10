"""Fields entity — CRUD for custom fields."""

from typing import Any, Dict, List

from cli_anything.mautic.utils.api_client import MauticClient


def list_fields(client: MauticClient, obj: str, **kwargs: Any) -> Dict[str, Any]:
     """List fields for an object type: GET /api/fields/{object}."""
    return client.list(f"fields/{obj}", **kwargs)


def get_field(client: MauticClient, obj: str, field_id: int) -> Dict[str, Any]:
     """Get field: GET /api/fields/{object}/{id}."""
    return client.get(f"fields/{obj}", field_id)


def create_field(client: MauticClient, obj: str, data: Dict[str, Any]) -> Dict[str, Any]:
     """Create field: POST /api/fields/{object}/new."""
    return client.create(f"fields/{obj}", data)


def edit_field(client: MauticClient, obj: str, field_id: int, data: Dict[str, Any],
               strict_mode: bool = False, ignore_missing: bool = False) -> Dict[str, Any]:
     """Edit field: PATCH /api/fields/{object}/{id}/edit."""
    return client.edit(f"fields/{obj}", field_id, data, strict_mode, ignore_missing)


def update_field(client: MauticClient, obj: str, field_id: int, data: Dict[str, Any],
                 strict_mode: bool = False, ignore_missing: bool = False) -> Dict[str, Any]:
     """Update field: PUT /api/fields/{object}/{id}/edit."""
    return client.update(f"fields/{obj}", field_id, data, strict_mode, ignore_missing)


def delete_field(client: MauticClient, obj: str, field_id: int) -> Dict[str, Any]:
     """Delete field: DELETE /api/fields/{object}/{id}/delete."""
    return client.delete(f"fields/{obj}", field_id)


def batch_delete_fields(client: MauticClient, obj: str, ids: List[int]) -> Dict[str, Any]:
     """Batch delete: POST /api/fields/{object}/batch/delete."""
    return client.batch_delete(f"fields/{obj}", ids)


def batch_edit_fields(client: MauticClient, obj: str, data: Dict[str, Any]) -> Dict[str, Any]:
     """Batch edit: PATCH /api/fields/{object}/batch/edit."""
    return client.batch_edit(f"fields/{obj}", data)


def batch_create_fields(client: MauticClient, obj: str, items: List[Dict[str, Any]]) -> Dict[str, Any]:
     """Batch create: POST /api/fields/{object}/batch/new."""
    return client.batch_create(f"fields/{obj}", items)
