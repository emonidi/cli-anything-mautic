"""Pages entity — CRUD operations."""
from typing import Any, Dict, List
from cli_anything.mautic.utils.api_client import MauticClient
def list_pages(client: MauticClient, **kwargs: Any) -> Dict[str, Any]:
    return client.list("pages", **kwargs)
def get_page(client: MauticClient, page_id: int) -> Dict[str, Any]:
    return client.get("pages", page_id)
def create_page(client: MauticClient, data: Dict[str, Any]) -> Dict[str, Any]:
    return client.create("pages", data)
def edit_page(client: MauticClient, page_id: int, data: Dict[str, Any], **kw):
    return client.edit("pages", page_id, data, **kw)
def update_page(client: MauticClient, page_id: int, data: Dict[str, Any], **kw):
    return client.update("pages", page_id, data, **kw)
def delete_page(client: MauticClient, page_id: int) -> Dict[str, Any]:
    return client.delete("pages", page_id)
def batch_delete_pages(client: MauticClient, ids: List[int]) -> Dict[str, Any]:
    return client.batch_delete("pages", ids)
def batch_edit_pages(client: MauticClient, data: Dict[str, Any]) -> Dict[str, Any]:
    return client.batch_edit("pages", data)
def batch_create_pages(client: MauticClient, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    return client.batch_create("pages", items)
