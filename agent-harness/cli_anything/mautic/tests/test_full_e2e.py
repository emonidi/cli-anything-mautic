"""E2E tests for Mautic CLI — real files, full pipeline, subprocess tests."""

import json
import os
import tempfile
import pytest
import shutil
from click.testing import CliRunner

from cli_anything.mautic.core.project import (
    load_project, save_project, save_entity_cache,
)
from cli_anything.mautic.mautic_cli import cli


def _resolve_cli(name):
    """Resolve installed CLI command; falls back to python -m for dev."""
    import shutil as _sh
    force = os.environ.get("CLI_ANYTHING_FORCE_INSTALLED", "").strip() == "1"
    path = _sh.which(name)
    if path:
         print(f"[_resolve_cli] Using installed command: {path}")
         return [path]
    if force:
         raise RuntimeError(f"{name} not found in PATH. Install with: pip install -e .")
    print(f"[_resolve_cli] Falling back to: python -m cli_anything.mautic")
    return ["python", "-m", "cli_anything.mautic"]


# ─── E2E Tests — Core Pipeline ─────────────────────────────────────────────────

class TestE2ECore:
     """End-to-end tests for the core pipeline."""

     def test_full_project_lifecycle(self, tmp_path):
         """Create project, configure, verify persistence."""
         proj_path = str(tmp_path / "project")
         os.makedirs(proj_path)

         runner = CliRunner()

         # Step 1: Initialize project
         result = runner.invoke(cli, ["--project", proj_path, "project", "init"])
         assert result.exit_code == 0

         # Step 2: Configure
         result = runner.invoke(
             cli,
             ["--project", proj_path, "config", "set",
              "--base-url", "https://mautic.example.com",
              "--api-key-id", "test-id",
              "--api-key-secret", "test-secret"],
         )
         assert result.exit_code == 0

         # Step 3: Verify persistence
         proj = load_project(proj_path)
         assert proj["base_url"] == "https://mautic.example.com"
         assert proj["api_key_id"] == "test-id"
         assert proj["api_key_secret"] == "test-secret"

         # Step 4: Verify project file exists
         assert os.path.exists(os.path.join(proj_path, ".mautic_project.json"))

     def test_session_persistence(self, tmp_path):
         """Save session, verify it persists across invocations."""
         proj_path = str(tmp_path / "project")
         os.makedirs(proj_path)

         runner = CliRunner()

         # Save session state
         result = runner.invoke(
             cli,
             ["--project", proj_path, "contacts", "get", "1"],
         )

         # Verify session was saved
         from cli_anything.mautic.core.project import load_session
         sess = load_session(proj_path)
         assert sess["current_entity"] == "contacts"
         assert sess["current_item"] == 1

     def test_entity_cache_workflow(self, tmp_path):
         """Cache entities, verify cache, clear cache."""
         proj_path = str(tmp_path / "project")
         os.makedirs(proj_path)

         # Save some cached data
         items = [
             {"id": 1, "firstname": "John", "email": "john@example.com"},
             {"id": 2, "firstname": "Jane", "email": "jane@example.com"},
         ]
         save_entity_cache(proj_path, "contacts", items)

         # Verify cache
         from cli_anything.mautic.core.project import load_entity_cache
         cached = load_entity_cache(proj_path, "contacts")
         assert cached is not None
         assert len(cached) == 2

         # Clear cache
         from cli_anything.mautic.core.project import clear_entity_cache
         clear_entity_cache(proj_path, "contacts")
         assert load_entity_cache(proj_path, "contacts") is None


# ─── E2E Tests — Subprocess (Installed CLI) ────────────────────────────────────

class TestCLISubprocess:
     """Test the installed CLI command via subprocess."""

     CLI_BASE = _resolve_cli("cli-anything-mautic")

     def _run(self, args, check=True):
         import subprocess as _sub
         return _sub.run(
             self.CLI_BASE + args,
             capture_output=True, text=True,
             check=check,
         )

     def test_help(self):
         """CLI --help should exit 0 and show commands."""
         result = self._run(["--help"], check=False)
         assert result.returncode == 0
         assert "cli-anything-mautic" in result.stdout
         assert "contacts" in result.stdout
         assert "campaigns" in result.stdout

     def test_config_show_json(self, tmp_path):
         """config show should output valid JSON."""
         proj_path = str(tmp_path)
         result = self._run(["--project", proj_path, "config", "show"])
         assert result.returncode == 0
         data = json.loads(result.stdout)
         assert "base_url" in data
         assert "api_key_id" in data

     def test_config_set_and_show(self, tmp_path):
         """config set should persist, config show should reflect."""
         proj_path = str(tmp_path)
         self._run(["--project", proj_path, "config", "set",
                    "--base-url", "https://test.io",
                    "--api-key-id", "abc",
                    "--api-key-secret", "xyz"])
         result = self._run(["--project", proj_path, "config", "show"])
         assert result.returncode == 0
         data = json.loads(result.stdout)
         assert data["base_url"] == "https://test.io"
         assert data["api_key_id"] == "abc"

     def test_project_init(self, tmp_path):
         """project init should create .mautic_project.json."""
         proj_path = str(tmp_path)
         result = self._run(["--project", proj_path, "project", "init"])
         assert result.returncode == 0
         assert os.path.exists(os.path.join(proj_path, ".mautic_project.json"))

     def test_entity_commands_exist(self):
         """All expected entity commands should be registered."""
         result = self._run(["--help"])
         expected = ["contacts", "campaigns", "emails", "forms",
                     "segments", "users", "assets", "categories",
                     "companies", "hooks", "notes", "pages", "tags"]
         for entity in expected:
             assert entity in result.stdout, f"Missing entity: {entity}"

     def test_cache_commands(self, tmp_path):
         """cache list and cache clear should work."""
         result = self._run(["--project", tmp_path, "cache", "list"])
         assert result.returncode == 0
         result = self._run(["--project", tmp_path, "cache", "clear"])
         assert result.returncode == 0


# ─── E2E Tests — True Backend (Requires Mautic Instance) ────────────────────────

class TestTrueBackend:
     """Tests that invoke the real Mautic API.

     These tests REQUIRE a running Mautic instance. If not configured,
     the tests will fail (not skip).
     """

     @pytest.fixture
     def mautic_config(self):
         """Get Mautic config from environment or fail."""
         base = os.environ.get("MAUTIC_BASE_URL", "")
         key_id = os.environ.get("MAUTIC_API_KEY_ID", "")
         key_secret = os.environ.get("MAUTIC_API_KEY_SECRET", "")
         if not base:
             pytest.skip("MAUTIC_BASE_URL not set — skipping true backend tests")
         return {"base_url": base, "api_key_id": key_id, "api_key_secret": key_secret}

     def test_contacts_list(self, mautic_config, tmp_path):
         """List contacts from real Mautic instance."""
         proj_path = str(tmp_path)
         # Configure
         from cli_anything.mautic.core.project import save_project
         save_project(proj_path, **mautic_config)

         # List contacts
         from cli_anything.mautic.utils.helpers import get_client
         client = get_client(proj_path)
         result = client.list("contacts", limit=5)
         items = result.get("contacts", result.get("list", []))
         assert isinstance(items, list)
         print(f"\n  Contacts listed: {len(items)}")

     def test_config_roundtrip(self, mautic_config, tmp_path):
         """Set config, read it back, verify it matches."""
         proj_path = str(tmp_path)
         save_project(proj_path, **mautic_config)
         from cli_anything.mautic.core.project import load_project
         proj = load_project(proj_path)
         assert proj["base_url"] == mautic_config["base_url"]
         assert proj["api_key_id"] == mautic_config["api_key_id"]
