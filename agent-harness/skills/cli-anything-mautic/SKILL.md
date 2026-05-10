---
name: "cli-anything-mautic"
description: "Stateful CLI harness for the Mautic marketing automation API. Provides one-shot commands and interactive REPL for managing contacts, campaigns, emails, forms, segments, and other entities. Uses direct HTTP calls to Mautic REST API (authenticated via API key)."
---

# cli-anything-mautic

Stateful CLI harness for the **Mautic** marketing automation API. Provides both one-shot commands and an interactive REPL mode for managing contacts, campaigns, emails, forms, segments, and other marketing entities.

## Installation

```bash
pip install -e /path/to/agent-harness
```

After installation, `cli-anything-mautic` is available in PATH.

## Prerequisites

- Python 3.10+
- A running Mautic instance with API access
- API Key (ID and Secret) from your Mautic instance

## Quick Start

### 1. Configure Your Mautic Instance

```bash
cli-anything-mautic config set \
    --base-url "https://yourcompany.com/mautic" \
    --api-key-id "your-api-key-id" \
    --api-key-secret "your-api-key-secret"
```

### 2. Initialize a Project

```bash
cli-anything-mautic project init -o /path/to/project
cd /path/to/project
```

### 3. Explore Entities

```bash
cli-anything-mautic contacts list --limit 10
cli-anything-mautic campaigns list
cli-anything-mautic emails list
cli-anything-mautic forms list
cli-anything-mautic segments list
```

## Command Reference

### Configuration

| Command | Description |
|---------|-------------|
| `config show` | Show current configuration (JSON output) |
| `config set --base-url <url> --api-key-id <id> --api-key-secret <secret>` | Set credentials |
| `config unset --base-url [--api-key-id] [--api-key-secret]` | Clear credentials |

### Project

| Command | Description |
|---------|-------------|
| `project init [-o <dir>]` | Initialize a new project directory |

### Entities (all support list/get/create/edit/update/delete/batch)

| Entity | Description |
|--------|-------------|
| `contacts` | Marketing contacts/leads |
| `campaigns` | Marketing campaigns |
| `emails` | Email templates |
| `forms` | Web forms |
| `segments` | Contact segments/lists |
| `users` | Mautic users |
| `assets` | Downloadable assets |
| `categories` | Item categories |
| `companies` | Company records |
| `pages` | Landing pages |
| `notes` | Contact notes |
| `tags` | Item tags |
| `stages` | Lifecycle stages |
| `reports` | Analytics reports |
| `hooks` | Webhooks |
| `themes` | Themes |
| `files` | Media files |
| `dynamiccontents` | Dynamic content blocks |
| `notifications` | System notifications |
| `points` | Point actions |
| `smses` | SMS templates |
| `tweets` | Social tweets |
| `messages` | Automated messages |
| `devices` | Contact devices |
| `fields` | Custom fields |

### Entity Commands

```bash
# List entities
cli-anything-mautic contacts list [--limit N] [--offset N] [-f key=value] [--json]

# Get single entity
cli-anything-mautic contacts get 1 [--json]

# Create entity
cli-anything-mautic contacts create --data '{"firstname":"John","email":"john@example.com"}' [--json]
cli-anything-mautic contacts create --file contact.json [--json]

# Edit entity (partial update)
cli-anything-mautic contacts edit 1 --data '{"email":"new@example.com"}' [--json]

# Update entity (full replace)
cli-anything-mautic contacts update 1 --data '{"firstname":"John","email":"john@example.com"}' [--json]

# Delete entity
cli-anything-mautic contacts delete 1 [--json]

# Batch operations
cli-anything-mautic contacts batch --op delete --data '{"ids":[1,2,3]}'
cli-anything-mautic contacts batch --op edit --data '{"1":{"email":"a@b.com"},"2":{"email":"c@d.com"}}'
cli-anything-mautic contacts batch --op update --data '...'
cli-anything-mautic contacts batch --op create --data '{"batch":[{...},{...}]}'
```

### Cache

| Command | Description |
|---------|-------------|
| `cache list` | List cached entities |
| `cache clear [entity]` | Clear entity cache (all if no entity specified) |

### Export

| Command | Description |
|---------|-------------|
| `export entities <type> [--format json|csv] [--limit N] [--pretty] [--json]` | Export entity data |

### REPL Mode

```bash
cli-anything-mautic
```

Interactive REPL with commands:
- `help` - Show command listing
- `help skill` - Read the skill definition
- `exit` / `quit` / `q` / `bye` - Exit REPL

## JSON Output

Every entity command supports `--json` for machine-readable output:

```bash
cli-anything-mautic contacts list --limit 5 --json
cli-anything-mautic contacts get 1 --json
cli-anything-mautic campaigns create --data '{"name":"Test"}' --json
```

## Agent Usage

Recommended workflow for AI agents:

1. **Configure**: `cli-anything-mautic config set --base-url <url> --api-key-id <id> --api-key-secret <secret>`
2. **Explore**: Use `--json` output for all queries
3. **Mutate**: Use one-shot commands with `--data` or `--file`
4. **Batch**: Use `batch --op <type> --data '{"ids":[1,2,3]}'` for bulk operations

## State Management

- Configuration is stored in `.mautic_project.json` in the project directory
- Session state (last accessed entity/item) auto-saves after mutations
- Entity caches stored in `.mautic_cache/` directory
- Use `--project <dir>` to target a specific project directory
