"""Points entity — CRUD operations."""
from typing import Any, Dict, List
from cli_anything.mautic.utils.api_client import MauticClient
def list(client: MauticClient, **kwargs: Any) -> Dict[str, Any]:
    return client.list("points", **kwargs)
def get(client: MauticClient, id: int) -> Dict[str, Any]:
    return client.get("points", id)
def create(client: MauticClient, data: Dict[str, Any]) -> Dict[str, Any]:
    return client.create("points", data)
def edit(client: MauticClient, id: int, data: Dict[str, Any], **kw):
    return client.edit("points", id, data, **kw)
def update(client: MauticClient, id: int, data: Dict[str, Any], **kw):
    return client.update("points", id, data, **kw)
def delete(client: MauticClient, id: int) -> Dict[str, Any]:
    return client.delete("points", id)
def batch_delete(client: MauticClient, ids: List[int]) -> Dict[str, Any]:
    return client.batch_delete("points", ids)
def batch_edit(client: MauticClient, data: Dict[str, Any]) -> Dict[str, Any]:
    return client.batch_edit("points", data)
def batch_create(client: MauticClient, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    return client.batch_create("points", items)
