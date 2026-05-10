"""Emails entity — CRUD and email-specific operations."""

from typing import Any, Dict, List

from cli_anything.mautic.utils.api_client import MauticClient


def list_emails(client: MauticClient, **kwargs: Any) -> Dict[str, Any]:
    """List emails: GET /api/emails."""
    return client.list("emails", **kwargs)


def get_email(client: MauticClient, email_id: int) -> Dict[str, Any]:
    """Get email: GET /api/emails/{id}."""
    return client.get("emails", email_id)


def create_email(client: MauticClient, data: Dict[str, Any]) -> Dict[str, Any]:
    """Create email: POST /api/emails/new."""
    return client.create("emails", data)


def edit_email(client: MauticClient, email_id: int, data: Dict[str, Any],
               strict_mode: bool = False, ignore_missing: bool = False) -> Dict[str, Any]:
    """Edit email: PATCH /api/emails/{id}/edit."""
    return client.edit("emails", email_id, data, strict_mode, ignore_missing)


def update_email(client: MauticClient, email_id: int, data: Dict[str, Any],
                 strict_mode: bool = False, ignore_missing: bool = False) -> Dict[str, Any]:
    """Update email: PUT /api/emails/{id}/edit."""
    return client.update("emails", email_id, data, strict_mode, ignore_missing)


def delete_email(client: MauticClient, email_id: int) -> Dict[str, Any]:
    """Delete email: DELETE /api/emails/{id}/delete."""
    return client.delete("emails", email_id)


def batch_delete_emails(client: MauticClient, ids: List[int]) -> Dict[str, Any]:
    """Batch delete: POST /api/emails/batch/delete."""
    return client.batch_delete("emails", ids)


def batch_edit_emails(client: MauticClient, data: Dict[str, Any]) -> Dict[str, Any]:
    """Batch edit: PATCH /api/emails/batch/edit."""
    return client.batch_edit("emails", data)


def batch_update_emails(client: MauticClient, data: Dict[str, Any]) -> Dict[str, Any]:
    """Batch update: PUT /api/emails/batch/edit."""
    return client.batch_update("emails", data)


def batch_create_emails(client: MauticClient, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Batch create: POST /api/emails/batch/new."""
    return client.batch_create("emails", items)


def send_email(client: MauticClient, email_id: int) -> Dict[str, Any]:
    """Send email to assigned lists: POST /api/emails/{id}/send."""
    return client.send_email(email_id)


def send_email_to_contact(client: MauticClient, email_id: int, contact_id: int) -> Dict[str, Any]:
    """Send email to specific contact: POST /api/emails/{id}/contact/{id}/send."""
    return client.send_email_to_contact(email_id, contact_id)
