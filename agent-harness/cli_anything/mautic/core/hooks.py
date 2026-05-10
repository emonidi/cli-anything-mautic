"""Hooks entity — CRUD operations."""

from typing import Any, Dict, List
from cli_anything.mautic.utils.api_client import MauticClient

def list_hooks(client: MauticClient, **kwargs: Any) -> Dict[str, Any]:
    return client.list("hooks", **kwargs)
def get_hook(client: MauticClient, hook_id: int) -> Dict[str, Any]:
    return client.get("hooks", hook_id)
def create_hook(client: MauticClient, data: Dict[str, Any]) -> Dict[str, Any]:
    return client.create("hooks", data)
def edit_hook(client: MauticClient, hook_id: int, data: Dict[str, Any], **kw):
    return client.edit("hooks", hook_id, data, **kw)
def update_hook(client: MauticClient, hook_id: int, data: Dict[str, Any], **kw):
    return client.update("hooks", hook_id, data, **kw)
def delete_hook(client: MauticClient, hook_id: int) -> Dict[str, Any]:
    return client.delete("hooks", hook_id)
def batch_delete_hooks(client: MauticClient, ids: List[int]) -> Dict[str, Any]:
    return client.batch_delete("hooks", ids)
def batch_edit_hooks(client: MauticClient, data: Dict[str, Any]) -> Dict[str, Any]:
    return client.batch_edit("hooks", data)
def batch_create_hooks(client: MauticClient, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    return client.batch_create("hooks", items)
def get_hooks_triggers(client: MauticClient) -> Dict[str, Any]:
    return client.get_hooks_triggers()
