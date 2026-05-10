"""Categories entity — CRUD operations."""

from typing import Any, Dict, List
from cli_anything.mautic.utils.api_client import MauticClient

def list_categories(client: MauticClient, **kwargs: Any) -> Dict[str, Any]:
    return client.list("categories", **kwargs)
def get_category(client: MauticClient, cat_id: int) -> Dict[str, Any]:
    return client.get("categories", cat_id)
def create_category(client: MauticClient, data: Dict[str, Any]) -> Dict[str, Any]:
    return client.create("categories", data)
def edit_category(client: MauticClient, cat_id: int, data: Dict[str, Any], **kw):
    return client.edit("categories", cat_id, data, **kw)
def update_category(client: MauticClient, cat_id: int, data: Dict[str, Any], **kw):
    return client.update("categories", cat_id, data, **kw)
def delete_category(client: MauticClient, cat_id: int) -> Dict[str, Any]:
    return client.delete("categories", cat_id)
def batch_delete_categories(client: MauticClient, ids: List[int]) -> Dict[str, Any]:
    return client.batch_delete("categories", ids)
def batch_edit_categories(client: MauticClient, data: Dict[str, Any]) -> Dict[str, Any]:
    return client.batch_edit("categories", data)
def batch_create_categories(client: MauticClient, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    return client.batch_create("categories", items)
