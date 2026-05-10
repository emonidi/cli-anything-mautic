# cli-anything-mautic

A stateful CLI harness for the **Mautic** marketing automation API. Provides both
one-shot commands and an interactive REPL mode for managing contacts, campaigns,
emails, forms, segments, and other marketing entities.

## Installation

### Prerequisites

- Python 3.10+
- A running Mautic instance with API access

### Install the CLI

```bash
pip install -e .
```

After installation, the `cli-anything-mautic` command will be available in your PATH.

### Verify Installation

```bash
cli-anything-mautic --help
cli-anything-mautic config show
```

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

### 4. Use the REPL

```bash
cli-anything-mautic
```

## Command Reference

### Configuration

| Command | Description |
|---------|-------------|
| `config show` | Show current configuration |
| `config set` | Set configuration values |
| `config unset` | Clear configuration values |

### Project

| Command | Description |
|---------|-------------|
| `project init -o <dir>` | Initialize a new project directory |

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
| `devices` | Contact devices |
| `dynamiccontents` | Dynamic content blocks |
| `fields` | Custom fields |
| `files` | Media files |
| `hooks` | Webhooks |
| `messages` | Automated messages |
| `notes` | Contact notes |
| `notifications` | System notifications |
| `pages` | Landing pages |
| `points` | Point actions |
| `reports` | Analytics reports |
| `smses` | SMS templates |
| `stages` | Lifecycle stages |
| `tags` | Item tags |
| `tweets` | Social tweets |
| `themes` | Themes |

### Helper Commands

| Command | Description |
|---------|-------------|
| `cache clear [entity]` | Clear entity cache |
| `cache list` | List cached entities |
| `export entities <type> [options]` | Export entity data |

## JSON Output

Every command supports the `--json` flag for machine-readable output:

```bash
cli-anything-mautic contacts list --limit 5 --json
cli-anything-mautic contacts get 1 --json
cli-anything-mautic campaigns create --data '{"name": "Test"}' --json
```

## REPL Mode

Run `cli-anything-mautic` without arguments to enter interactive REPL mode:

```
   ================================
   MAUTIC CLI  v1.0.0
   Python Mautic API Harness
   ================================
   Skill: /path/to/skills/cli-anything-mautic/SKILL.md
   Type help skill to read the skill definition.

  Type help for commands, exit to quit.

  (mautic myinstance)>
```

### REPL Commands

- `help` — Show command listing
- `help skill` — Read the skill definition
- `exit` / `quit` / `q` / `bye` — Exit REPL

## Auto-Save & --dry-run

Session state is automatically saved after each mutation (create, edit, update, delete).
Use `--dry-run` on mutation commands to preview changes without persisting them.

## Agent Usage

For AI agents, the recommended workflow is:

1. **Configure**: `cli-anything-mautic config set --base-url <url> --api-key-id <id> --api-key-secret <secret>`
2. **Explore**: Use `--json` output for all queries
3. **Mutate**: Use one-shot commands with `--data` or `--file`
4. **Batch**: Use `batch --op <type> --data '{"ids": [1,2,3]}'` for bulk operations

See `skills/cli-anything-mautic/SKILL.md` for the full agent skill definition.
