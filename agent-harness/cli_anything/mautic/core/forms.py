"""Forms entity — CRUD and form-specific operations."""

from typing import Any, Dict, List

from cli_anything.mautic.utils.api_client import MauticClient


def list_forms(client: MauticClient, **kwargs: Any) -> Dict[str, Any]:
    """List forms: GET /api/forms."""
    return client.list("forms", **kwargs)


def get_form(client: MauticClient, form_id: int) -> Dict[str, Any]:
    """Get form: GET /api/forms/{id}."""
    return client.get("forms", form_id)


def create_form(client: MauticClient, data: Dict[str, Any]) -> Dict[str, Any]:
    """Create form: POST /api/forms/new."""
    return client.create("forms", data)


def edit_form(client: MauticClient, form_id: int, data: Dict[str, Any],
              strict_mode: bool = False, ignore_missing: bool = False) -> Dict[str, Any]:
    """Edit form: PATCH /api/forms/{id}/edit."""
    return client.edit("forms", form_id, data, strict_mode, ignore_missing)


def update_form(client: MauticClient, form_id: int, data: Dict[str, Any],
                strict_mode: bool = False, ignore_missing: bool = False) -> Dict[str, Any]:
    """Update form: PUT /api/forms/{id}/edit."""
    return client.update("forms", form_id, data, strict_mode, ignore_missing)


def delete_form(client: MauticClient, form_id: int) -> Dict[str, Any]:
    """Delete form: DELETE /api/forms/{id}/delete."""
    return client.delete("forms", form_id)


def batch_delete_forms(client: MauticClient, ids: List[int]) -> Dict[str, Any]:
    """Batch delete: POST /api/forms/batch/delete."""
    return client.batch_delete("forms", ids)


def batch_edit_forms(client: MauticClient, data: Dict[str, Any]) -> Dict[str, Any]:
    """Batch edit: PATCH /api/forms/batch/edit."""
    return client.batch_edit("forms", data)


def batch_update_forms(client: MauticClient, data: Dict[str, Any]) -> Dict[str, Any]:
    """Batch update: PUT /api/forms/batch/edit."""
    return client.batch_update("forms", data)


def batch_create_forms(client: MauticClient, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Batch create: POST /api/forms/batch/new."""
    return client.batch_create("forms", items)


def get_form_submissions(client: MauticClient, form_id: int, **kwargs: Any) -> Dict[str, Any]:
    """Get form submissions: GET /api/forms/{id}/submissions."""
    return client.get_form_submissions(form_id)


def get_form_submission(client: MauticClient, form_id: int, submission_id: int) -> Dict[str, Any]:
    """Get form submission: GET /api/forms/{id}/submissions/{sid}."""
    return client.get_form_submission(form_id, submission_id)


def get_form_contact_submissions(client: MauticClient, form_id: int, contact_id: int) -> Dict[str, Any]:
    """Get form submissions for contact: GET /api/forms/{id}/submissions/contact/{id}."""
    return client.get_form_contact_submissions(form_id, contact_id)


def delete_form_fields(client: MauticClient, form_id: int, fields: List[str]) -> Dict[str, Any]:
    """Delete form fields: DELETE /api/forms/{id}/fields/delete."""
    return client.delete_form_fields(form_id, fields)


def delete_form_actions(client: MauticClient, form_id: int, actions: List[str]) -> Dict[str, Any]:
    """Delete form actions: DELETE /api/forms/{id}/actions/delete."""
    return client.delete_form_actions(form_id, actions)
