"""Devices entity — CRUD operations."""

from typing import Any, Dict, List
from cli_anything.mautic.utils.api_client import MauticClient

def list_devices(client: MauticClient, **kwargs: Any) -> Dict[str, Any]:
    return client.list("devices", **kwargs)
def get_device(client: MauticClient, device_id: int) -> Dict[str, Any]:
    return client.get("devices", device_id)
def create_device(client: MauticClient, data: Dict[str, Any]) -> Dict[str, Any]:
    return client.create("devices", data)
def edit_device(client: MauticClient, device_id: int, data: Dict[str, Any], **kw):
    return client.edit("devices", device_id, data, **kw)
def update_device(client: MauticClient, device_id: int, data: Dict[str, Any], **kw):
    return client.update("devices", device_id, data, **kw)
def delete_device(client: MauticClient, device_id: int) -> Dict[str, Any]:
    return client.delete("devices", device_id)
def batch_delete_devices(client: MauticClient, ids: List[int]) -> Dict[str, Any]:
    return client.batch_delete("devices", ids)
def batch_edit_devices(client: MauticClient, data: Dict[str, Any]) -> Dict[str, Any]:
    return client.batch_edit("devices", data)
def batch_create_devices(client: MauticClient, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    return client.batch_create("devices", items)
