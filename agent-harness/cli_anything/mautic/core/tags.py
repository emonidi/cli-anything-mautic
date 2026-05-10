"""Tags entity — CRUD operations."""
from typing import Any, Dict, List
from cli_anything.mautic.utils.api_client import MauticClient
def list(client: MauticClient, **kwargs: Any) -> Dict[str, Any]:
    return client.list("tags", **kwargs)
def get(client: MauticClient, id: int) -> Dict[str, Any]:
    return client.get("tags", id)
def create(client: MauticClient, data: Dict[str, Any]) -> Dict[str, Any]:
    return client.create("tags", data)
def edit(client: MauticClient, id: int, data: Dict[str, Any], **kw):
    return client.edit("tags", id, data, **kw)
def update(client: MauticClient, id: int, data: Dict[str, Any], **kw):
    return client.update("tags", id, data, **kw)
def delete(client: MauticClient, id: int) -> Dict[str, Any]:
    return client.delete("tags", id)
def batch_delete(client: MauticClient, ids: List[int]) -> Dict[str, Any]:
    return client.batch_delete("tags", ids)
def batch_edit(client: MauticClient, data: Dict[str, Any]) -> Dict[str, Any]:
    return client.batch_edit("tags", data)
def batch_create(client: MauticClient, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    return client.batch_create("tags", items)
