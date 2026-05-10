"""Segments entity — CRUD and segment-specific operations."""

from typing import Any, Dict, List

from cli_anything.mautic.utils.api_client import MauticClient


def list_segments(client: MauticClient, **kwargs: Any) -> Dict[str, Any]:
    """List segments: GET /api/segments."""
    return client.list("segments", **kwargs)


def get_segment(client: MauticClient, segment_id: int) -> Dict[str, Any]:
    """Get segment: GET /api/segments/{id}."""
    return client.get("segments", segment_id)


def create_segment(client: MauticClient, data: Dict[str, Any]) -> Dict[str, Any]:
    """Create segment: POST /api/segments/new."""
    return client.create("segments", data)


def edit_segment(client: MauticClient, segment_id: int, data: Dict[str, Any],
                 strict_mode: bool = False, ignore_missing: bool = False) -> Dict[str, Any]:
    """Edit segment: PATCH /api/segments/{id}/edit."""
    return client.edit("segments", segment_id, data, strict_mode, ignore_missing)


def update_segment(client: MauticClient, segment_id: int, data: Dict[str, Any],
                   strict_mode: bool = False, ignore_missing: bool = False) -> Dict[str, Any]:
    """Update segment: PUT /api/segments/{id}/edit."""
    return client.update("segments", segment_id, data, strict_mode, ignore_missing)


def delete_segment(client: MauticClient, segment_id: int) -> Dict[str, Any]:
    """Delete segment: DELETE /api/segments/{id}/delete."""
    return client.delete("segments", segment_id)


def batch_delete_segments(client: MauticClient, ids: List[int]) -> Dict[str, Any]:
     """Batch delete: POST /api/segments/batch/delete."""
    return client.batch_delete("segments", ids)


def batch_edit_segments(client: MauticClient, data: Dict[str, Any]) -> Dict[str, Any]:
     """Batch edit: PATCH /api/segments/batch/edit."""
    return client.batch_edit("segments", data)


def batch_update_segments(client: MauticClient, data: Dict[str, Any]) -> Dict[str, Any]:
     """Batch update: PUT /api/segments/batch/edit."""
    return client.batch_update("segments", data)


def batch_create_segments(client: MauticClient, items: List[Dict[str, Any]]) -> Dict[str, Any]:
     """Batch create: POST /api/segments/batch/new."""
    return client.batch_create("segments", items)


def add_contact(client: MauticClient, segment_id: int, contact_id: int) -> Dict[str, Any]:
     """Add contact to segment: POST /api/segments/{id}/contact/{id}/add."""
    return client.add_to_segment(segment_id, contact_id)


def remove_contact(client: MauticClient, segment_id: int, contact_id: int) -> Dict[str, Any]:
     """Remove contact from segment: POST /api/segments/{id}/contact/{id}/remove."""
    return client.remove_from_segment(segment_id, contact_id)


def add_contacts(client: MauticClient, segment_id: int, contact_ids: List[int]) -> Dict[str, Any]:
     """Add contacts to segment: POST /api/segments/{id}/contacts/add."""
    return client._request("POST", f"segments/{segment_id}/contacts/add", json_data={"ids": contact_ids})
