"""Campaigns entity — CRUD and campaign-specific operations."""

from typing import Any, Dict, List

from cli_anything.mautic.utils.api_client import MauticClient


def list_campaigns(client: MauticClient, **kwargs: Any) -> Dict[str, Any]:
    """List campaigns: GET /api/campaigns."""
    return client.list("campaigns", **kwargs)


def get_campaign(client: MauticClient, campaign_id: int) -> Dict[str, Any]:
    """Get campaign: GET /api/campaigns/{id}."""
    return client.get("campaigns", campaign_id)


def create_campaign(client: MauticClient, data: Dict[str, Any]) -> Dict[str, Any]:
    """Create campaign: POST /api/campaigns/new."""
    return client.create("campaigns", data)


def edit_campaign(client: MauticClient, campaign_id: int, data: Dict[str, Any],
                  strict_mode: bool = False, ignore_missing: bool = False) -> Dict[str, Any]:
    """Edit campaign: PATCH /api/campaigns/{id}/edit."""
    return client.edit("campaigns", campaign_id, data, strict_mode, ignore_missing)


def update_campaign(client: MauticClient, campaign_id: int, data: Dict[str, Any],
                    strict_mode: bool = False, ignore_missing: bool = False) -> Dict[str, Any]:
    """Update campaign: PUT /api/campaigns/{id}/edit."""
    return client.update("campaigns", campaign_id, data, strict_mode, ignore_missing)


def delete_campaign(client: MauticClient, campaign_id: int) -> Dict[str, Any]:
    """Delete campaign: DELETE /api/campaigns/{id}/delete."""
    return client.delete("campaigns", campaign_id)


def batch_delete_campaigns(client: MauticClient, ids: List[int]) -> Dict[str, Any]:
    """Batch delete: POST /api/campaigns/batch/delete."""
    return client.batch_delete("campaigns", ids)


def batch_edit_campaigns(client: MauticClient, data: Dict[str, Any]) -> Dict[str, Any]:
    """Batch edit: PATCH /api/campaigns/batch/edit."""
    return client.batch_edit("campaigns", data)


def batch_update_campaigns(client: MauticClient, data: Dict[str, Any]) -> Dict[str, Any]:
    """Batch update: PUT /api/campaigns/batch/edit."""
    return client.batch_update("campaigns", data)


def batch_create_campaigns(client: MauticClient, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Batch create: POST /api/campaigns/batch/new."""
    return client.batch_create("campaigns", items)


def add_contact(client: MauticClient, campaign_id: int, contact_id: int) -> Dict[str, Any]:
    """Add contact to campaign: POST /api/campaigns/{id}/contact/{id}/add."""
    return client.add_to_campaign(campaign_id, contact_id)


def remove_contact(client: MauticClient, campaign_id: int, contact_id: int) -> Dict[str, Any]:
    """Remove contact from campaign: POST /api/campaigns/{id}/contact/{id}/remove."""
    return client.remove_from_campaign(campaign_id, contact_id)


def get_campaign_contacts(client: MauticClient, campaign_id: int) -> Dict[str, Any]:
    """Get campaign contacts: GET /api/campaigns/{id}/contacts."""
    return client.get_campaign_contacts(campaign_id)


def clone_campaign(client: MauticClient, campaign_id: int) -> Dict[str, Any]:
    """Clone campaign: POST /api/campaigns/clone/{id}."""
    return client.clone_campaign(campaign_id)


def get_campaign_events(client: MauticClient, campaign_id: int) -> Dict[str, Any]:
    """Get campaign events: GET /api/campaigns/events?campaignId={id}."""
    return client.get_campaign_events(campaign_id)


def get_campaign_event(client: MauticClient, campaign_id: int, event_id: int,
                       contact_id: int) -> Dict[str, Any]:
    """Get campaign event for contact: GET /api/campaigns/{id}/events/contact/{id}."""
    return client.get_campaign_event(campaign_id, event_id, contact_id)
