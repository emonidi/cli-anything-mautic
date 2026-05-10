"""Notifications entity — CRUD operations."""
from typing import Any, Dict, List
from cli_anything.mautic.utils.api_client import MauticClient
def list(client: MauticClient, **kwargs: Any) -> Dict[str, Any]:
    return client.list("notifications", **kwargs)
def get(client: MauticClient, id: int) -> Dict[str, Any]:
    return client.get("notifications", id)
def create(client: MauticClient, data: Dict[str, Any]) -> Dict[str, Any]:
    return client.create("notifications", data)
def edit(client: MauticClient, id: int, data: Dict[str, Any], **kw):
    return client.edit("notifications", id, data, **kw)
def update(client: MauticClient, id: int, data: Dict[str, Any], **kw):
    return client.update("notifications", id, data, **kw)
def delete(client: MauticClient, id: int) -> Dict[str, Any]:
    return client.delete("notifications", id)
def batch_delete(client: MauticClient, ids: List[int]) -> Dict[str, Any]:
    return client.batch_delete("notifications", ids)
def batch_edit(client: MauticClient, data: Dict[str, Any]) -> Dict[str, Any]:
    return client.batch_edit("notifications", data)
def batch_create(client: MauticClient, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    return client.batch_create("notifications", items)
