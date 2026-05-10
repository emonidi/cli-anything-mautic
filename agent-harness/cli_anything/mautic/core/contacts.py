"""Contacts entity — list, get, create, edit, delete, and contact-specific operations."""

from typing import Any, Dict, List, Optional

from cli_anything.mautic.utils.api_client import MauticClient


def list_contacts(client: MauticClient, **kwargs: Any) -> Dict[str, Any]:
    """List contacts: GET /api/contacts."""
    return client.list("contacts", **kwargs)


def get_contact(client: MauticClient, contact_id: int) -> Dict[str, Any]:
    """Get contact by ID: GET /api/contacts/{id}."""
    return client.get("contacts", contact_id)


def create_contact(client: MauticClient, data: Dict[str, Any]) -> Dict[str, Any]:
    """Create contact: POST /api/contacts/new."""
    return client.create("contacts", data)


def edit_contact(client: MauticClient, contact_id: int, data: Dict[str, Any],
                 strict_mode: bool = False, ignore_missing: bool = False) -> Dict[str, Any]:
    """Edit contact: PATCH /api/contacts/{id}/edit."""
    return client.edit("contacts", contact_id, data, strict_mode, ignore_missing)


def update_contact(client: MauticClient, contact_id: int, data: Dict[str, Any],
                   strict_mode: bool = False, ignore_missing: bool = False) -> Dict[str, Any]:
    """Update contact (create if not exists): PUT /api/contacts/{id}/edit."""
    return client.update("contacts", contact_id, data, strict_mode, ignore_missing)


def delete_contact(client: MauticClient, contact_id: int) -> Dict[str, Any]:
    """Delete contact: DELETE /api/contacts/{id}/delete."""
    return client.delete("contacts", contact_id)


def batch_delete_contacts(client: MauticClient, ids: List[int]) -> Dict[str, Any]:
    """Batch delete contacts: POST /api/contacts/batch/delete."""
    return client.batch_delete("contacts", ids)


def batch_edit_contacts(client: MauticClient, data: Dict[str, Any]) -> Dict[str, Any]:
    """Batch edit contacts: PATCH /api/contacts/batch/edit."""
    return client.batch_edit("contacts", data)


def batch_update_contacts(client: MauticClient, data: Dict[str, Any]) -> Dict[str, Any]:
    """Batch update contacts: PUT /api/contacts/batch/edit."""
    return client.batch_update("contacts", data)


def batch_create_contacts(client: MauticClient, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Batch create contacts: POST /api/contacts/batch/new."""
    return client.batch_create("contacts", items)


def get_contact_activity(client: MauticClient, contact_id: int) -> Dict[str, Any]:
    """Get contact activity: GET /api/contacts/{id}/activity."""
    return client.contact_activity(contact_id)


def get_contact_campaigns(client: MauticClient, contact_id: int) -> Dict[str, Any]:
    """Get contact campaigns: GET /api/contacts/{id}/campaigns."""
    return client.contact_campaigns(contact_id)


def get_contact_companies(client: MauticClient, contact_id: int) -> Dict[str, Any]:
    """Get contact companies: GET /api/contacts/{id}/companies."""
    return client.contact_companies(contact_id)


def get_contact_segments(client: MauticClient, contact_id: int) -> Dict[str, Any]:
    """Get contact segments: GET /api/contacts/{id}/segments."""
    return client.contact_segments(contact_id)


def get_contact_notes(client: MauticClient, contact_id: int) -> Dict[str, Any]:
    """Get contact notes: GET /api/contacts/{id}/notes."""
    return client.contact_notes(contact_id)


def get_contact_devices(client: MauticClient, contact_id: int) -> Dict[str, Any]:
    """Get contact devices: GET /api/contacts/{id}/devices."""
    return client.contact_devices(contact_id)


def add_to_campaign(client: MauticClient, campaign_id: int, contact_id: int) -> Dict[str, Any]:
    """Add contact to campaign: POST /api/campaigns/{id}/contact/{id}/add."""
    return client.add_to_campaign(campaign_id, contact_id)


def remove_from_campaign(client: MauticClient, campaign_id: int, contact_id: int) -> Dict[str, Any]:
    """Remove contact from campaign: POST /api/campaigns/{id}/contact/{id}/remove."""
    return client.remove_from_campaign(campaign_id, contact_id)


def add_to_segment(client: MauticClient, segment_id: int, contact_id: int) -> Dict[str, Any]:
    """Add contact to segment: POST /api/segments/{id}/contact/{id}/add."""
    return client.add_to_segment(segment_id, contact_id)


def remove_from_segment(client: MauticClient, segment_id: int, contact_id: int) -> Dict[str, Any]:
    """Remove contact from segment: POST /api/segments/{id}/contact/{id}/remove."""
    return client.remove_from_segment(segment_id, contact_id)


def add_dnc(client: MauticClient, contact_id: int, channel: str) -> Dict[str, Any]:
    """Add DNC: POST /api/contacts/{id}/dnc/{channel}/add."""
    return client.add_dnc(contact_id, channel)


def remove_dnc(client: MauticClient, contact_id: int, channel: str) -> Dict[str, Any]:
    """Remove DNC: POST /api/contacts/{id}/dnc/{channel}/remove."""
    return client.remove_dnc(contact_id, channel)


def add_points(client: MauticClient, contact_id: int, delta: int) -> Dict[str, Any]:
    """Add points: POST /api/contacts/{id}/points/+/{delta}."""
    return client.add_points(contact_id, delta)


def subtract_points(client: MauticClient, contact_id: int, delta: int) -> Dict[str, Any]:
    """Subtract points: POST /api/contacts/{id}/points/-/{delta}."""
    return client.subtract_points(contact_id, delta)


def list_all(client: MauticClient, **kwargs: Any) -> Dict[str, Any]:
    """Alias for list_contacts."""
    return list_contacts(client, **kwargs)


def get_all(id: int, **kwargs: Any) -> Dict[str, Any]:
    """Alias for get_contact."""
    return get_contact(client, id, **kwargs)
