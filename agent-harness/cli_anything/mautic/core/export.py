"""Export module — export entity data to CSV/JSON."""

import csv
import io
import json
from typing import Any, Dict, List, Optional


def export_to_json(data: Any, pretty: bool = True) -> str:
    """Export data as JSON string."""
    if pretty:
        return json.dumps(data, indent=2, default=str)
    return json.dumps(data, default=str)


def export_to_csv(data: List[Dict[str, Any]], filename: str = "export.csv") -> str:
    """Export a list of dicts as CSV string."""
    if not data:
        return ""
    fieldnames = list(data[0].keys())
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()


def export_entity(entity_name: str, items: List[Dict[str, Any]],
                   fmt: str = "json", pretty: bool = True) -> str:
    """Export a list of entities in the requested format."""
    if fmt == "csv":
        return export_to_csv(items)
    return export_to_json({"entity": entity_name, "items": items}, pretty)
