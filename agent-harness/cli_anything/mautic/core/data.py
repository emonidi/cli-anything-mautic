"""Data entity — widget data, stats, custom fields, owners, smart segments."""
from typing import Any, Dict
from cli_anything.mautic.utils.api_client import MauticClient

def get_widget_data(client: MauticClient, data_type: str = "") -> Dict[str, Any]:
     """Get widget data: GET /api/data[{type}]."""
    return client.get_widget_data(data_type)

def get_stats(client: MauticClient, table: str) -> Dict[str, Any]:
     """Get table stats: GET /api/stats/{table}."""
    return client.get_stats(table)

def get_custom_fields(client: MauticClient) -> Dict[str, Any]:
     """Get custom fields: GET /api/contacts/list/fields."""
    return client.get_custom_fields()

def get_owners(client: MauticClient) -> Dict[str, Any]:
     """Get owners: GET /api/contacts/list/owners."""
    return client.get_owners()

def get_smart_segments(client: MauticClient) -> Dict[str, Any]:
     """Get smart segments: GET /api/contacts/list/segments."""
    return client.get_smart_segments()
