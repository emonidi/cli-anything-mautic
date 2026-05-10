"""Project management — load/save Mautic instance config and entity state."""

import json
import os
from typing import Any, Dict, List, Optional

PROJECT_FILENAME = ".mautic_project.json"
SESSION_FILENAME = ".mautic_session.json"
GLOBAL_PROJECT_FILENAME = ".mautic_project.json"  # in ~/.mautic/


def _project_path(root: str) -> str:
    """Return the path to the project config file in root."""
    return os.path.join(root, PROJECT_FILENAME)


def _session_path(root: str) -> str:
    """Return the path to the session file in root."""
    return os.path.join(root, SESSION_FILENAME)


def _locked_save_json(path: str, data: Dict[str, Any], **kwargs) -> None:
    """Atomically write JSON with exclusive file locking."""
    try:
        f = open(path, "r+")
    except FileNotFoundError:
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        f = open(path, "w")
    with f:
        _locked = False
        try:
            import fcntl
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            _locked = True
        except (ImportError, OSError):
            pass
        try:
            f.seek(0)
            f.truncate()
            json.dump(data, f, **kwargs)
            f.flush()
        finally:
            if _locked:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)


def _global_config_path() -> Optional[str]:
    """Return path to the global config file (~/.mautic/.mautic_project.json)."""
    global_path = os.path.join(os.path.expanduser("~"), ".mautic", GLOBAL_PROJECT_FILENAME)
    return global_path if os.path.exists(global_path) else None


def load_project(project_path: Optional[str] = None) -> Dict[str, Any]:
    """Load project config from file, or return empty config.

    Falls back to a global config in ~/.mautic/.mautic_project.json
    if no local config exists in the target directory.

    Returns dict with keys: base_url, api_key_id, api_key_secret, api_version.
    """
    if project_path is None:
        project_path = os.getcwd()
    path = _project_path(project_path)
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    # Fallback to global config
    global_path = _global_config_path()
    if global_path is not None:
        with open(global_path, "r") as f:
            return json.load(f)
    return {"base_url": "", "api_key_id": "", "api_key_secret": "", "oauth2_token_endpoint": "", "api_version": "2"}


def save_project(project_path: Optional[str] = None, **kwargs: Any) -> None:
    """Save project config. kwargs override defaults (base_url, api_key_id, api_key_secret)."""
    if project_path is None:
        project_path = os.getcwd()
    proj = load_project(project_path)
    proj.update(kwargs)
    _locked_save_json(_project_path(project_path), proj, indent=2)


def load_session(project_path: Optional[str] = None) -> Dict[str, Any]:
    """Load session state (current_entity, history, undo_stack)."""
    if project_path is None:
        project_path = os.getcwd()
    path = _session_path(project_path)
    if not os.path.exists(path):
        return {"current_entity": None, "current_item": None, "history": [], "undo_stack": []}
    with open(path, "r") as f:
        return json.load(f)


def save_session(project_path: Optional[str] = None, **kwargs: Any) -> None:
    """Save session state."""
    if project_path is None:
        project_path = os.getcwd()
    sess = load_session(project_path)
    sess.update(kwargs)
    _locked_save_json(_session_path(project_path), sess, indent=2)


def get_entity_dir(project_path: Optional[str] = None) -> str:
    """Return the entities cache directory path."""
    if project_path is None:
        project_path = os.getcwd()
    dir_path = os.path.join(project_path, ".mautic_entities")
    os.makedirs(dir_path, exist_ok=True)
    return dir_path


def save_entity_cache(project_path: Optional[str], entity: str, data: Any) -> None:
    """Save a list of entities to the cache directory."""
    dir_path = get_entity_dir(project_path)
    path = os.path.join(dir_path, f"{entity}.json")
    _locked_save_json(path, {"entity": entity, "fetched_at": str(__import__("datetime").datetime.now().isoformat()), "items": data if isinstance(data, list) else [data]})


def load_entity_cache(project_path: Optional[str], entity: str) -> Optional[List]:
    """Load cached entities, or None if no cache exists."""
    if project_path is None:
        project_path = os.getcwd()
    path = os.path.join(get_entity_dir(project_path), f"{entity}.json")
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return json.load(f).get("items")


def clear_entity_cache(project_path: Optional[str], entity: Optional[str] = None) -> None:
    """Clear cache for one entity or all entities."""
    dir_path = get_entity_dir(project_path)
    if entity:
        path = os.path.join(dir_path, f"{entity}.json")
        if os.path.exists(path):
            os.remove(path)
    else:
        for fname in os.listdir(dir_path):
            if fname.endswith(".json"):
                os.remove(os.path.join(dir_path, fname))


def has_credentials(project_path: Optional[str] = None) -> bool:
    """Check if project has valid credentials."""
    proj = load_project(project_path)
    return bool(proj.get("base_url")) and (bool(proj.get("api_key_id")) or bool(proj.get("base_url")))
