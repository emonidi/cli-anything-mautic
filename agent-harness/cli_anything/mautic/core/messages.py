"""Messages entity — CRUD operations."""
from typing import Any, Dict, List
from cli_anything.mautic.utils.api_client import MauticClient
def list_messages(client: MauticClient, **kwargs: Any) -> Dict[str, Any]:
    return client.list("messages", **kwargs)
def get_message(client: MauticClient, msg_id: int) -> Dict[str, Any]:
    return client.get("messages", msg_id)
def create_message(client: MauticClient, data: Dict[str, Any]) -> Dict[str, Any]:
    return client.create("messages", data)
def edit_message(client: MauticClient, msg_id: int, data: Dict[str, Any], **kw):
    return client.edit("messages", msg_id, data, **kw)
def update_message(client: MauticClient, msg_id: int, data: Dict[str, Any], **kw):
    return client.update("messages", msg_id, data, **kw)
def delete_message(client: MauticClient, msg_id: int) -> Dict[str, Any]:
    return client.delete("messages", msg_id)
def batch_delete_messages(client: MauticClient, ids: List[int]) -> Dict[str, Any]:
    return client.batch_delete("messages", ids)
def batch_edit_messages(client: MauticClient, data: Dict[str, Any]) -> Dict[str, Any]:
    return client.batch_edit("messages", data)
def batch_create_messages(client: MauticClient, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    return client.batch_create("messages", items)
