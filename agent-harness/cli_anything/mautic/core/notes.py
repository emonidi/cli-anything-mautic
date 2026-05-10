"""Notes entity — CRUD operations."""
from typing import Any, Dict, List
from cli_anything.mautic.utils.api_client import MauticClient
def list_notes(client: MauticClient, **kwargs: Any) -> Dict[str, Any]:
    return client.list("notes", **kwargs)
def get_note(client: MauticClient, note_id: int) -> Dict[str, Any]:
    return client.get("notes", note_id)
def create_note(client: MauticClient, data: Dict[str, Any]) -> Dict[str, Any]:
    return client.create("notes", data)
def edit_note(client: MauticClient, note_id: int, data: Dict[str, Any], **kw):
    return client.edit("notes", note_id, data, **kw)
def update_note(client: MauticClient, note_id: int, data: Dict[str, Any], **kw):
    return client.update("notes", note_id, data, **kw)
def delete_note(client: MauticClient, note_id: int) -> Dict[str, Any]:
    return client.delete("notes", note_id)
def batch_delete_notes(client: MauticClient, ids: List[int]) -> Dict[str, Any]:
    return client.batch_delete("notes", ids)
def batch_edit_notes(client: MauticClient, data: Dict[str, Any]) -> Dict[str, Any]:
    return client.batch_edit("notes", data)
def batch_create_notes(client: MauticClient, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    return client.batch_create("notes", items)
