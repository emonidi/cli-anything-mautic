"""Unit tests for Mautic CLI core modules — synthetic data, no external deps."""

import json
import os
import tempfile
import pytest
from click.testing import CliRunner

from cli_anything.mautic.core.project import (
    load_project, save_project, load_session, save_session,
    has_credentials, get_entity_dir, clear_entity_cache,
    save_entity_cache, load_entity_cache,
)
from cli_anything.mautic.core.export import export_to_json, export_to_csv, export_entity
from cli_anything.mautic.utils.helpers import get_client, get_project
from cli_anything.mautic.mautic_cli import cli


@pytest.fixture
def tmp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as d:
        yield d


@pytest.fixture
def runner():
    """Click test runner."""
    return CliRunner()


# ─── Project Tests ─────────────────────────────────────────────────────────────

class TestProject:
     def test_save_and_load_project(self, tmp_dir):
         save_project(tmp_dir, base_url="https://test.mautic.io", api_key_id="abc", api_key_secret="xyz")
         proj = load_project(tmp_dir)
         assert proj["base_url"] == "https://test.mautic.io"
         assert proj["api_key_id"] == "abc"
         assert proj["api_key_secret"] == "xyz"

     def test_default_project(self, tmp_dir):
         proj = load_project(tmp_dir)
         assert proj["base_url"] == ""
         assert proj["api_version"] == "2"

     def test_has_credentials_true(self, tmp_dir):
         save_project(tmp_dir, base_url="https://test.mautic.io", api_key_id="abc")
         assert has_credentials(tmp_dir) is True

     def test_has_credentials_false(self, tmp_dir):
         assert has_credentials(tmp_dir) is False

     def test_update_project(self, tmp_dir):
         save_project(tmp_dir, base_url="https://old.io")
         save_project(tmp_dir, base_url="https://new.io")
         proj = load_project(tmp_dir)
         assert proj["base_url"] == "https://new.io"


class TestSession:
     def test_save_and_load_session(self, tmp_dir):
         save_session(tmp_dir, current_entity="contacts", current_item=42, history=["list", "get"])
         sess = load_session(tmp_dir)
         assert sess["current_entity"] == "contacts"
         assert sess["current_item"] == 42
         assert sess["history"] == ["list", "get"]

     def test_default_session(self, tmp_dir):
         sess = load_session(tmp_dir)
         assert sess["current_entity"] is None
         assert sess["current_item"] is None

     def test_update_session(self, tmp_dir):
         save_session(tmp_dir, current_entity="campaigns")
         save_session(tmp_dir, current_entity="contacts", current_item=1)
         sess = load_session(tmp_dir)
         assert sess["current_entity"] == "contacts"
         assert sess["current_item"] == 1


class TestEntityCache:
     def test_save_and_load_cache(self, tmp_dir):
         items = [{"id": 1, "name": "Contact 1"}, {"id": 2, "name": "Contact 2"}]
         save_entity_cache(tmp_dir, "contacts", items)
         cached = load_entity_cache(tmp_dir, "contacts")
         assert cached is not None
         assert len(cached) == 2
         assert cached[0]["name"] == "Contact 1"

     def test_load_missing_cache(self, tmp_dir):
         assert load_entity_cache(tmp_dir, "nonexistent") is None

     def test_clear_entity_cache(self, tmp_dir):
         items = [{"id": 1}]
         save_entity_cache(tmp_dir, "contacts", items)
         clear_entity_cache(tmp_dir, "contacts")
         assert load_entity_cache(tmp_dir, "contacts") is None

     def test_clear_all_cache(self, tmp_dir):
         save_entity_cache(tmp_dir, "contacts", [{"id": 1}])
         save_entity_cache(tmp_dir, "campaigns", [{"id": 2}])
         clear_entity_cache(tmp_dir)
         assert load_entity_cache(tmp_dir, "contacts") is None
         assert load_entity_cache(tmp_dir, "campaigns") is None

     def test_get_entity_dir_creates_it(self, tmp_dir):
         cache_dir = get_entity_dir(tmp_dir)
         assert os.path.isdir(cache_dir)


# ─── Export Tests ───────────────────────────────────────────────────────────────

class TestExport:
     def test_export_to_json(self):
         data = {"id": 1, "name": "Test"}
         result = export_to_json(data)
         parsed = json.loads(result)
         assert parsed["id"] == 1
         assert parsed["name"] == "Test"

     def test_export_to_json_pretty(self):
         data = {"id": 1}
         result = export_to_json(data, pretty=True)
         assert "\n" in result  # Pretty print has newlines

     def test_export_to_json_compact(self):
         data = {"id": 1}
         result = export_to_json(data, pretty=False)
         assert "\n" not in result

     def test_export_to_csv(self):
         items = [{"id": 1, "name": "A"}, {"id": 2, "name": "B"}]
         result = export_to_csv(items)
         assert "id,name" in result
         assert "1,A" in result
         assert "2,B" in result

     def test_export_to_csv_empty(self):
         assert export_to_csv([]) == ""

     def test_export_entity_json(self):
         items = [{"id": 1}]
         result = export_entity("contacts", items, fmt="json")
         assert '"entity"' in result
         assert '"contacts"' in result

     def test_export_entity_csv(self):
         items = [{"id": 1, "name": "Test"}]
         result = export_entity("contacts", items, fmt="csv")
         assert "id,name" in result


# ─── Helpers Tests ──────────────────────────────────────────────────────────────

class TestHelpers:
     def test_get_project_empty(self, tmp_dir):
         proj = get_project(tmp_dir)
         assert proj["base_url"] == ""

     def test_get_client_raises_without_url(self, tmp_dir):
         with pytest.raises(RuntimeError, match="No Mautic instance configured"):
             get_client(tmp_dir)


# ─── CLI Tests ───────────────────────────────────────────────────────────────────

class TestCLIBasic:
     def test_help(self):
         result = CliRunner().invoke(cli, ["--help"])
         assert result.exit_code == 0
         assert "cli-anything-mautic" in result.output

     def test_config_show_empty(self, tmp_dir):
         result = CliRunner().invoke(cli, ["--project", tmp_dir, "config", "show"])
         assert result.exit_code == 0
         data = json.loads(result.stdout)
         assert data["base_url"] == ""

     def test_config_set(self, tmp_dir):
         result = CliRunner().invoke(
             cli,
             ["--project", tmp_dir, "config", "set",
              "--base-url", "https://test.io",
              "--api-key-id", "abc",
              "--api-key-secret", "xyz"],
         )
         assert result.exit_code == 0
         proj = load_project(tmp_dir)
         assert proj["base_url"] == "https://test.io"

     def test_config_unset(self, tmp_dir):
         save_project(tmp_dir, base_url="https://test.io")
         result = CliRunner().invoke(cli, ["--project", tmp_dir, "config", "unset", "--base-url"])
         assert result.exit_code == 0
         proj = load_project(tmp_dir)
         assert proj["base_url"] == ""

     def test_project_init(self, tmp_dir):
         result = CliRunner().invoke(cli, ["--project", tmp_dir, "project", "init"])
         assert result.exit_code == 0
         proj_path = os.path.join(tmp_dir, ".mautic_project.json")
         assert os.path.exists(proj_path)

     def test_cache_clear_all(self, tmp_dir):
         save_entity_cache(tmp_dir, "contacts", [{"id": 1}])
         result = CliRunner().invoke(cli, ["--project", tmp_dir, "cache", "clear"])
         assert result.exit_code == 0

     def test_cache_list_empty(self, tmp_dir):
         result = CliRunner().invoke(cli, ["--project", tmp_dir, "cache", "list"])
         assert result.exit_code == 0

     def test_entity_group_exists(self):
         result = CliRunner().invoke(cli, ["--help"])
         assert "contacts" in result.output
         assert "campaigns" in result.output
         assert "emails" in result.output
         assert "forms" in result.output
         assert "segments" in result.output
         assert "users" in result.output

     def test_entity_list_requires_api(self, tmp_dir):
         save_project(tmp_dir, base_url="https://nonexistent.io", api_key_id="x")
         result = CliRunner().invoke(cli, ["--project", tmp_dir, "contacts", "list"])
         assert result.exit_code != 0  # No actual Mautic instance
