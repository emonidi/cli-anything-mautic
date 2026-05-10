"""Reports entity — list and get reports."""
from typing import Any, Dict
from cli_anything.mautic.utils.api_client import MauticClient

def list_reports(client: MauticClient, **kwargs: Any) -> Dict[str, Any]:
    """List reports: GET /api/reports."""
    return client.list("reports", **kwargs)

def get_report(client: MauticClient, report_id: int) -> Dict[str, Any]:
    """Get compiled report: GET /api/reports/{id}."""
    return client.get_report(report_id)
