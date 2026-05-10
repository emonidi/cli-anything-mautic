"""Companies entity — CRUD operations."""

from typing import Any, Dict, List
from cli_anything.mautic.utils.api_client import MauticClient

def list_companies(client: MauticClient, **kwargs: Any) -> Dict[str, Any]:
    return client.list("companies", **kwargs)
def get_company(client: MauticClient, company_id: int) -> Dict[str, Any]:
    return client.get("companies", company_id)
def create_company(client: MauticClient, data: Dict[str, Any]) -> Dict[str, Any]:
    return client.create("companies", data)
def edit_company(client: MauticClient, company_id: int, data: Dict[str, Any], **kw):
    return client.edit("companies", company_id, data, **kw)
def update_company(client: MauticClient, company_id: int, data: Dict[str, Any], **kw):
    return client.update("companies", company_id, data, **kw)
def delete_company(client: MauticClient, company_id: int) -> Dict[str, Any]:
    return client.delete("companies", company_id)
def batch_delete_companies(client: MauticClient, ids: List[int]) -> Dict[str, Any]:
    return client.batch_delete("companies", ids)
def batch_edit_companies(client: MauticClient, data: Dict[str, Any]) -> Dict[str, Any]:
    return client.batch_edit("companies", data)
def batch_create_companies(client: MauticClient, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    return client.batch_create("companies", items)
def add_contact(client: MauticClient, company_id: int, contact_id: int) -> Dict[str, Any]:
    return client.add_to_company(company_id, contact_id)
def remove_contact(client: MauticClient, company_id: int, contact_id: int) -> Dict[str, Any]:
    return client.remove_from_company(company_id, contact_id)
