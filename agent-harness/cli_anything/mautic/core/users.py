"""Users entity — CRUD operations."""

from typing import Any, Dict, List

from cli_anything.mautic.utils.api_client import MauticClient


def list_users(client: MauticClient, **kwargs: Any) -> Dict[str, Any]:
    """List users: GET /api/users."""
    return client.list("users", **kwargs)


def get_user(client: MauticClient, user_id: int) -> Dict[str, Any]:
    """Get user: GET /api/users/{id}."""
    return client.get("users", user_id)


def create_user(client: MauticClient, data: Dict[str, Any]) -> Dict[str, Any]:
    """Create user: POST /api/users/new."""
    return client.create("users", data)


def edit_user(client: MauticClient, user_id: int, data: Dict[str, Any],
              strict_mode: bool = False, ignore_missing: bool = False) -> Dict[str, Any]:
     """Edit user: PATCH /api/users/{id}/edit."""
    return client.edit("users", user_id, data, strict_mode, ignore_missing)


def update_user(client: MauticClient, user_id: int, data: Dict[str, Any],
                strict_mode: bool = False, ignore_missing: bool = False) -> Dict[str, Any]:
     """Update user: PUT /api/users/{id}/edit."""
    return client.update("users", user_id, data, strict_mode, ignore_missing)


def delete_user(client: MauticClient, user_id: int) -> Dict[str, Any]:
     """Delete user: DELETE /api/users/{id}/delete."""
    return client.delete("users", user_id)


def batch_delete_users(client: MauticClient, ids: List[int]) -> Dict[str, Any]:
     """Batch delete: POST /api/users/batch/delete."""
    return client.batch_delete("users", ids)


def batch_edit_users(client: MauticClient, data: Dict[str, Any]) -> Dict[str, Any]:
     """Batch edit: PATCH /api/users/batch/edit."""
    return client.batch_edit("users", data)


def batch_update_users(client: MauticClient, data: Dict[str, Any]) -> Dict[str, Any]:
     """Batch update: PUT /api/users/batch/edit."""
    return client.batch_update("users", data)


def batch_create_users(client: MauticClient, items: List[Dict[str, Any]]) -> Dict[str, Any]:
     """Batch create: POST /api/users/batch/new."""
    return client.batch_create("users", items)


def check_permission(client: MauticClient, user_id: int, permissions: List[str]) -> Dict[str, Any]:
     """Check user permission: POST /api/users/{id}/permissioncheck."""
    return client.check_user_permission(user_id, permissions)


def get_self(client: MauticClient) -> Dict[str, Any]:
     """Get current user: GET /api/users/self."""
    return client.get_self()
