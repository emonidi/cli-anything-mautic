"""Files entity — list, upload, delete files from Mautic /media directory."""
import os as _os
from typing import Any, Dict
from cli_anything.mautic.utils.api_client import MauticClient

def list_dir(client: MauticClient, directory: str) -> Dict[str, Any]:
     """List files: GET /api/files/{dir}."""
    return client.list_files(directory)

def upload(client: MauticClient, directory: str, file_path: str) -> Dict[str, Any]:
     """Upload file: POST /api/files/{dir}/new."""
    return client.upload_file(directory, file_path)

def delete(client: MauticClient, directory: str, filename: str) -> Dict[str, Any]:
     """Delete file: DELETE /api/files/{dir}/{file}/delete."""
    return client.delete_file(directory, filename)
