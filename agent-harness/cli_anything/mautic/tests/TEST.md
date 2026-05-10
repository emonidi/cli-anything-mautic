# Mautic CLI — Test Plan & Results

## Test Plan

### test_core.py — Unit Tests (31 tests)

| Class | Tests | Description |
|-------|-------|-------------|
| TestProject | 5 | Save/load project, default values, credentials check, update |
| TestSession | 3 | Save/load session, default values, state update |
| TestEntityCache | 5 | Save/load cache, missing cache, clear single/all |
| TestExport | 6 | JSON/CSV export, pretty/compact, entity export |
| TestHelpers | 2 | get_project, get_client (raises without URL) |
| TestCLIBasic | 8 | Help, config CRUD, project init, cache, entity groups, list requires api |

### test_full_e2e.py — E2E Tests (11 tests)

| Class | Tests | Description |
|-------|-------|-------------|
| TestE2ECore | 3 | Project lifecycle, session persistence, cache workflow |
| TestCLISubprocess | 6 | Installed CLI via subprocess: help, config, project, entities, cache |
| TestTrueBackend | 2 | Real Mautic API (requires MAUTIC_BASE_URL env) |

### Workflow Scenarios

1. **Project Initialization**: Create project dir → init → configure → verify persistence
2. **Session Management**: Get contact → verify session state → verify persistence
3. **Cache Workflow**: Save cache → load cache → clear cache → verify empty
4. **Subprocess CLI**: Test installed CLI from any directory with real command

## Test Results

### Run 1 — 2026-05-10

```
============================= test session starts ==============================
platform darwin -- Python 3.14.4, pytest-9.0.3, pluggy-1.6.0
collected 42 items

test_core.py::TestProject::test_save_and_load_project PASSED
test_core.py::TestProject::test_default_project PASSED
test_core.py::TestProject::test_has_credentials_true PASSED
test_core.py::TestProject::test_has_credentials_false PASSED
test_core.py::TestProject::test_update_project PASSED
test_core.py::TestSession::test_save_and_load_session PASSED
test_core.py::TestSession::test_default_session PASSED
test_core.py::TestSession::test_update_session PASSED
test_core.py::TestEntityCache::test_save_and_load_cache PASSED
test_core.py::TestEntityCache::test_load_missing_cache PASSED
test_core.py::TestEntityCache::test_clear_entity_cache PASSED
test_core.py::TestEntityCache::test_clear_all_cache PASSED
test_core.py::TestEntityCache::test_get_entity_dir_creates_it PASSED
test_core.py::TestExport::test_export_to_json PASSED
test_core.py::TestExport::test_export_to_json_pretty PASSED
test_core.py::TestExport::test_export_to_json_compact PASSED
test_core.py::TestExport::test_export_to_csv PASSED
test_core.py::TestExport::test_export_to_csv_empty PASSED
test_core.py::TestExport::test_export_entity_json PASSED
test_core.py::TestExport::test_export_entity_csv PASSED
test_core.py::TestHelpers::test_get_project_empty PASSED
test_core.py::TestHelpers::test_get_client_raises_without_url PASSED
test_core.py::TestCLIBasic::test_help PASSED
test_core.py::TestCLIBasic::test_config_show_empty PASSED
test_core.py::TestCLIBasic::test_config_set PASSED
test_core.py::TestCLIBasic::test_config_unset PASSED
test_core.py::TestCLIBasic::test_project_init PASSED
test_core.py::TestCLIBasic::test_cache_clear_all PASSED
test_core.py::TestCLIBasic::test_cache_list_empty PASSED
test_core.py::TestCLIBasic::test_entity_group_exists PASSED
test_core.py::TestCLIBasic::test_entity_list_requires_api PASSED
test_full_e2e.py::TestE2ECore::test_full_project_lifecycle PASSED
test_full_e2e.py::TestE2ECore::test_session_persistence PASSED
test_full_e2e.py::TestE2ECore::test_entity_cache_workflow PASSED
test_full_e2e.py::TestCLISubprocess::test_help PASSED
test_full_e2e.py::TestCLISubprocess::test_config_show_json PASSED
test_full_e2e.py::TestCLISubprocess::test_config_set_and_show PASSED
test_full_e2e.py::TestCLISubprocess::test_project_init PASSED
test_full_e2e.py::TestCLISubprocess::test_entity_commands_exist PASSED
test_full_e2e.py::TestCLISubprocess::test_cache_commands PASSED
test_full_e2e.py::TestTrueBackend::test_contacts_list SKIPPED
test_full_e2e.py::TestTrueBackend::test_config_roundtrip SKIPPED

======================== 40 passed, 2 skipped in 4.84s =========================
```

### Summary

- **40 passed** — All unit tests and E2E tests passing
- **2 skipped** — True backend tests (require `MAUTIC_BASE_URL` env var)
- **0 failed** — All tests passing

### Known Limitations

- True backend tests (`TestTrueBackend`) require a running Mautic instance; skipped when `MAUTIC_BASE_URL` is not set
