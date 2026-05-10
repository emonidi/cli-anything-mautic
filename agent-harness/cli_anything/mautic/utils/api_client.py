"""Mautic API client — wraps direct HTTP calls to the Mautic REST API.

This module makes actual HTTP requests to a Mautic instance. It does NOT
reimplement the API logic; it simply provides the transport layer.
"""

import os
import time
from typing import Any, Dict, List, Optional

import requests


class MauticClient:
    """HTTP client for a Mautic instance."""

    def __init__(self, base_url: str, api_key_id: str = "", api_key_secret: str = "",
                 oauth2_token_endpoint: str = "", api_version: str = "2", timeout: int = 30, max_retries: int = 3):
        self.base_url = base_url.rstrip("/")
        self.api_key_id = api_key_id
        self.api_key_secret = api_key_secret
        self.oauth2_token_endpoint = oauth2_token_endpoint
        self.timeout = timeout
        self.max_retries = max_retries
        # OAuth2 cache
        self._access_token: Optional[str] = None
        self._token_expiry: float = 0

    def _ensure_oauth2_token(self) -> str:
        """Fetch or refresh OAuth2 access token. Returns the token string."""
        import urllib.parse
        now = time.time()
        if self._access_token and now < self._token_expiry - 60:     # 60s buffer
            return self._access_token
        resp = requests.post(self.oauth2_token_endpoint, data={
             "grant_type": "client_credentials",
             "client_id": self.api_key_id,
             "client_secret": self.api_key_secret,
        })
        resp.raise_for_status()
        token_data = resp.json()
        self._access_token = token_data["access_token"]
        self._token_expiry = now + token_data.get("expires_in", 3600)
        return self._access_token

    @property
    def session(self) -> requests.Session:
        """Create a configured requests session."""
        s = requests.Session()
        s.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })
        # OAuth2 Bearer token auth (preferred)
        if self.oauth2_token_endpoint:
            token = self._ensure_oauth2_token()
            s.headers["Authorization"] = f"Bearer {token}"
        elif self.api_key_id and self.api_key_secret:
            # Basic Auth fallback
            s.auth = (self.api_key_id, self.api_key_secret)
        return s

    def _url(self, path: str) -> str:
        """Build full URL for an API path."""
        if path.startswith("/"):
            path = path[1:]
        base = self.base_url.rstrip("/")
        if base.endswith("/api"):
            base = base[:-4]
        return f"{base}/api/{path}"

    def _request(self, method: str, path: str, params: Optional[Dict] = None,
                 json_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make an HTTP request with retry logic."""
        url = self._url(path)
        sess = self.session
        last_err = None

        for attempt in range(self.max_retries + 1):
            try:
                resp = sess.request(
                    method, url,
                    params=params,
                    json=json_data,
                    timeout=self.timeout,
                )
                resp.raise_for_status()
                return resp.json()
            except (requests.RequestException, requests.HTTPError) as exc:
                last_err = exc
                if attempt < self.max_retries:
                    time.sleep(0.5 * (2 ** attempt))
        raise RuntimeError(f"API request failed after {self.max_retries + 1} retries: {last_err}")

    # -- CRUD helpers --

    def list(self, entity: str, **kwargs: Any) -> Dict[str, Any]:
        """List entities: GET /api/{entity}."""
        params = {k: v for k, v in kwargs.items() if v is not None}
        return self._request("GET", f"{entity}", params=params)

    def get(self, entity: str, item_id: int, **kwargs: Any) -> Dict[str, Any]:
        """Get single entity: GET /api/{entity}/{id}."""
        params = {k: v for k, v in kwargs.items() if v is not None}
        return self._request("GET", f"{entity}/{item_id}", params=params)

    def create(self, entity: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create entity: POST /api/{entity}/new."""
        return self._request("POST", f"{entity}/new", json_data=data)

    def edit(self, entity: str, item_id: int, data: Dict[str, Any],
             strict_mode: bool = False, ignore_missing: bool = False) -> Dict[str, Any]:
        """Edit entity: PATCH /api/{entity}/{id}/edit."""
        params = {}
        if strict_mode:
            params["strict"] = 1
        if ignore_missing:
            params["ignoreMissing"] = 1
        return self._request("PATCH", f"{entity}/{item_id}/edit", params=params or None, json_data=data)

    def update(self, entity: str, item_id: int, data: Dict[str, Any],
               strict_mode: bool = False, ignore_missing: bool = False) -> Dict[str, Any]:
        """Update entity (create if not exists): PUT /api/{entity}/{id}/edit."""
        params = {}
        if strict_mode:
            params["strict"] = 1
        if ignore_missing:
            params["ignoreMissing"] = 1
        return self._request("PUT", f"{entity}/{item_id}/edit", params=params or None, json_data=data)

    def delete(self, entity: str, item_id: int) -> Dict[str, Any]:
        """Delete entity: DELETE /api/{entity}/{id}/delete."""
        return self._request("DELETE", f"{entity}/{item_id}/delete")

    # -- Batch operations --

    def batch_delete(self, entity: str, ids: List[int]) -> Dict[str, Any]:
        """Batch delete: POST /api/{entity}/batch/delete."""
        return self._request("POST", f"{entity}/batch/delete", json_data={"ids": ids})

    def batch_edit(self, entity: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Batch edit: PATCH /api/{entity}/batch/edit."""
        return self._request("PATCH", f"{entity}/batch/edit", json_data=data)

    def batch_update(self, entity: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Batch update: PUT /api/{entity}/batch/edit."""
        return self._request("PUT", f"{entity}/batch/edit", json_data=data)

    def batch_create(self, entity: str, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Batch create: POST /api/{entity}/batch/new."""
        return self._request("POST", f"{entity}/batch/new", json_data={"batch": items})

    # -- Specialized endpoints --

    def contact_activity(self, contact_id: int) -> Dict[str, Any]:
        """Get contact activity: GET /api/contacts/{id}/activity."""
        return self._request("GET", f"contacts/{contact_id}/activity")

    def contact_campaigns(self, contact_id: int) -> Dict[str, Any]:
        """Get contact campaigns: GET /api/contacts/{id}/campaigns."""
        return self._request("GET", f"contacts/{contact_id}/campaigns")

    def contact_companies(self, contact_id: int) -> Dict[str, Any]:
        """Get contact companies: GET /api/contacts/{id}/companies."""
        return self._request("GET", f"contacts/{contact_id}/companies")

    def contact_segments(self, contact_id: int) -> Dict[str, Any]:
        """Get contact segments: GET /api/contacts/{id}/segments."""
        return self._request("GET", f"contacts/{contact_id}/segments")

    def contact_notes(self, contact_id: int) -> Dict[str, Any]:
        """Get contact notes: GET /api/contacts/{id}/notes."""
        return self._request("GET", f"contacts/{contact_id}/notes")

    def contact_devices(self, contact_id: int) -> Dict[str, Any]:
        """Get contact devices: GET /api/contacts/{id}/devices."""
        return self._request("GET", f"contacts/{contact_id}/devices")

    def add_to_campaign(self, campaign_id: int, contact_id: int) -> Dict[str, Any]:
        """Add contact to campaign: POST /api/campaigns/{id}/contact/{id}/add."""
        return self._request("POST", f"campaigns/{campaign_id}/contact/{contact_id}/add")

    def remove_from_campaign(self, campaign_id: int, contact_id: int) -> Dict[str, Any]:
        """Remove contact from campaign: POST /api/campaigns/{id}/contact/{id}/remove."""
        return self._request("POST", f"campaigns/{campaign_id}/contact/{contact_id}/remove")

    def add_to_segment(self, segment_id: int, contact_id: int) -> Dict[str, Any]:
        """Add contact to segment: POST /api/segments/{id}/contact/{id}/add."""
        return self._request("POST", f"segments/{segment_id}/contact/{contact_id}/add")

    def remove_from_segment(self, segment_id: int, contact_id: int) -> Dict[str, Any]:
        """Remove contact from segment: POST /api/segments/{id}/contact/{id}/remove."""
        return self._request("POST", f"segments/{segment_id}/contact/{contact_id}/remove")

    def send_email_to_contact(self, email_id: int, contact_id: int) -> Dict[str, Any]:
        """Send email to contact: POST /api/emails/{id}/contact/{id}/send."""
        return self._request("POST", f"emails/{email_id}/contact/{contact_id}/send")

    def send_email(self, email_id: int) -> Dict[str, Any]:
        """Send email to assigned lists: POST /api/emails/{id}/send."""
        return self._request("POST", f"emails/{email_id}/send")

    def get_form_submissions(self, form_id: int) -> Dict[str, Any]:
        """Get form submissions: GET /api/forms/{id}/submissions."""
        return self._request("GET", f"forms/{form_id}/submissions")

    def get_form_submission(self, form_id: int, submission_id: int) -> Dict[str, Any]:
        """Get specific form submission: GET /api/forms/{id}/submissions/{sid}."""
        return self._request("GET", f"forms/{form_id}/submissions/{submission_id}")

    def get_form_contact_submissions(self, form_id: int, contact_id: int) -> Dict[str, Any]:
        """Get form submissions for contact: GET /api/forms/{id}/submissions/contact/{id}."""
        return self._request("GET", f"forms/{form_id}/submissions/contact/{contact_id}")

    def delete_form_fields(self, form_id: int, fields: List[str]) -> Dict[str, Any]:
        """Delete form fields: DELETE /api/forms/{id}/fields/delete."""
        return self._request("DELETE", f"forms/{form_id}/fields/delete", json_data={"fields": fields})

    def delete_form_actions(self, form_id: int, actions: List[str]) -> Dict[str, Any]:
        """Delete form actions: DELETE /api/forms/{id}/actions/delete."""
        return self._request("DELETE", f"forms/{form_id}/actions/delete", json_data={"actions": actions})

    def add_to_company(self, company_id: int, contact_id: int) -> Dict[str, Any]:
        """Add contact to company: POST /api/companies/{id}/contact/{id}/add."""
        return self._request("POST", f"companies/{company_id}/contact/{contact_id}/add")

    def remove_from_company(self, company_id: int, contact_id: int) -> Dict[str, Any]:
        """Remove contact from company: POST /api/companies/{id}/contact/{id}/remove."""
        return self._request("POST", f"companies/{company_id}/contact/{contact_id}/remove")

    def add_dnc(self, contact_id: int, channel: str) -> Dict[str, Any]:
        """Add DNC: POST /api/contacts/{id}/dnc/{channel}/add."""
        return self._request("POST", f"contacts/{contact_id}/dnc/{channel}/add")

    def remove_dnc(self, contact_id: int, channel: str) -> Dict[str, Any]:
        """Remove DNC: POST /api/contacts/{id}/dnc/{channel}/remove."""
        return self._request("POST", f"contacts/{contact_id}/dnc/{channel}/remove")

    def add_points(self, contact_id: int, delta: int) -> Dict[str, Any]:
        """Add points: POST /api/contacts/{id}/points/+/{delta}."""
        path = f"contacts/{contact_id}/points/+/{delta}"
        return self._request("POST", path)

    def subtract_points(self, contact_id: int, delta: int) -> Dict[str, Any]:
        """Subtract points: POST /api/contacts/{id}/points/-/{delta}."""
        path = f"contacts/{contact_id}/points/-/{delta}"
        return self._request("POST", path)

    def get_custom_fields(self) -> Dict[str, Any]:
        """Get custom fields: GET /api/contacts/list/fields."""
        return self._request("GET", "contacts/list/fields")

    def get_owners(self) -> Dict[str, Any]:
        """Get owners: GET /api/contacts/list/owners."""
        return self._request("GET", "contacts/list/owners")

    def get_smart_segments(self) -> Dict[str, Any]:
        """Get smart segments: GET /api/contacts/list/segments."""
        return self._request("GET", "contacts/list/segments")

    def get_widget_data(self, data_type: str = "") -> Dict[str, Any]:
        """Get widget data: GET /api/data[{type}]."""
        path = f"data/{data_type}" if data_type else "data"
        return self._request("GET", path)

    def get_stats(self, table: str) -> Dict[str, Any]:
        """Get table stats: GET /api/stats/{table}."""
        return self._request("GET", f"stats/{table}")

    def get_reports(self) -> Dict[str, Any]:
        """Get reports: GET /api/reports."""
        return self._request("GET", "reports")

    def get_report(self, report_id: int) -> Dict[str, Any]:
        """Get compiled report: GET /api/reports/{id}."""
        return self._request("GET", f"reports/{report_id}")

    def get_themes(self) -> Dict[str, Any]:
        """Get themes: GET /api/themes."""
        return self._request("GET", "themes")

    def install_theme(self, zip_path: str) -> Dict[str, Any]:
        """Install theme from zip: POST /api/themes/new (multipart)."""
        with open(zip_path, "rb") as f:
            files = {"file": ("theme.zip", f, "application/zip")}
            return self.session.post(f"{self._url('themes/new')}", files=files).json()

    def delete_theme(self, theme_name: str) -> Dict[str, Any]:
        """Delete theme: DELETE /api/themes/{theme}/delete."""
        return self._request("DELETE", f"themes/{theme_name}/delete")

    def get_theme(self, theme_name: str) -> Dict[str, Any]:
        """Get theme zip: GET /api/themes/{theme}."""
        resp = self.session.get(f"{self._url('themes')}/{theme_name}")
        resp.raise_for_status()
        return {"content": resp.content, "content_type": resp.headers.get("Content-Type")}

    def list_files(self, directory: str) -> Dict[str, Any]:
        """List files: GET /api/files/{dir}."""
        return self._request("GET", f"files/{directory}")

    def upload_file(self, directory: str, file_path: str) -> Dict[str, Any]:
        """Upload file: POST /api/files/{dir}/new."""
        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f, "application/octet-stream")}
            return self.session.post(f"{self._url(f'files/{directory}/new')}", files=files).json()

    def delete_file(self, directory: str, filename: str) -> Dict[str, Any]:
        """Delete file: DELETE /api/files/{dir}/{file}/delete."""
        return self._request("DELETE", f"files/{directory}/{filename}/delete")

    def get_hooks_triggers(self) -> Dict[str, Any]:
        """Get hook triggers: GET /api/hooks/triggers."""
        return self._request("GET", "hooks/triggers")

    def clone_campaign(self, campaign_id: int) -> Dict[str, Any]:
        """Clone campaign: POST /api/campaigns/clone/{id}."""
        return self._request("POST", f"campaigns/clone/{campaign_id}")

    def get_focus_js(self, focus_id: int) -> Dict[str, Any]:
        """Get focus page JS: POST /api/focus/{id}/js."""
        return self._request("POST", f"focus/{focus_id}/js")

    def get_contact_activity(self, contact_id: int) -> Dict[str, Any]:
        """Get single contact activity: GET /api/contacts/{id}/activity."""
        return self._request("GET", f"contacts/{contact_id}/activity")

    def get_campaign_contacts(self, campaign_id: int) -> Dict[str, Any]:
        """Get campaign contacts: GET /api/campaigns/{id}/contacts."""
        return self._request("GET", f"campaigns/{campaign_id}/contacts")

    def get_campaign_event(self, campaign_id: int, event_id: int, contact_id: int) -> Dict[str, Any]:
        """Get campaign event for contact: GET /api/campaigns/{id}/events/contact/{id}."""
        return self._request("GET", f"campaigns/{campaign_id}/events/contact/{contact_id}")

    def get_campaign_events(self, campaign_id: int) -> Dict[str, Any]:
        """Get campaign events: GET /api/campaigns/events."""
        params = {"campaignId": campaign_id}
        return self._request("GET", "campaigns/events", params=params)

    def get_campaign_event_detail(self, event_id: int) -> Dict[str, Any]:
        """Get campaign event detail: GET /api/campaigns/events/{id}."""
        return self._request("GET", f"campaigns/events/{event_id}")

    def get_email_stats(self, email_id: int) -> Dict[str, Any]:
        """Get email stats: GET /api/emails/{id}."""
        return self._get_email_stats(email_id)

    def _get_email_stats(self, email_id: int) -> Dict[str, Any]:
        """Internal: get email stats."""
        return self._request("GET", f"emails/{email_id}")

    def check_user_permission(self, user_id: int, permissions: List[str]) -> Dict[str, Any]:
        """Check user permission: POST /api/users/{id}/permissioncheck."""
        return self._request("POST", f"users/{id}/permissioncheck", json_data={"permissions": permissions})

    def get_self(self) -> Dict[str, Any]:
        """Get current user: GET /api/users/self."""
        return self._request("GET", "users/self")

    def get_user(self, user_id: int) -> Dict[str, Any]:
        """Get user: GET /api/users/{id}."""
        return self._request("GET", f"users/{user_id}")

    def create_user(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create user: POST /api/users/new."""
        return self._request("POST", "users/new", json_data=data)

    def edit_user(self, user_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Edit user: PATCH /api/users/{id}/edit."""
        return self._request("PATCH", f"users/{user_id}/edit", json_data=data)

    def update_user(self, user_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update user (create if not exists): PUT /api/users/{id}/edit."""
        return self._request("PUT", f"users/{user_id}/edit", json_data=data)

    def delete_user(self, user_id: int) -> Dict[str, Any]:
        """Delete user: DELETE /api/users/{id}/delete."""
        return self._request("DELETE", f"users/{user_id}/delete")

    def list_users(self, **kwargs: Any) -> Dict[str, Any]:
        """List users: GET /api/users."""
        params = {k: v for k, v in kwargs.items() if v is not None}
        return self._request("GET", "users", params=params)

