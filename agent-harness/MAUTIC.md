# Mautic CLI — Software-Specific SOP

## Overview

This CLI harness wraps the **Mautic REST API** (open-source marketing automation platform).
It provides a stateful, agent-friendly interface for managing contacts, campaigns,
emails, forms, segments, and other marketing entities.

## Backend

- **Software**: Mautic (https://mautic.org)
- **API**: RESTful JSON API at `/api/{entity}` endpoints
- **Auth**: HTTP Basic Auth (API Key ID + API Key Secret) or Basic Auth (username/password)
- **Swagger Spec**: https://github.com/G2Rail/mautic-swagger-client
- **Native CLI**: None — Mautic is a PHP web application with API-only interface

## API Architecture

The Mautic API follows a consistent pattern across all entities:

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List | GET | `/api/{entity}` |
| Get | GET | `/api/{entity}/{id}` |
| Create | POST | `/api/{entity}/new` |
| Edit | PATCH | `/api/{entity}/{id}/edit` |
| Update (create if missing) | PUT | `/api/{entity}/{id}/edit` |
| Delete | DELETE | `/api/{entity}/{id}/delete` |
| Batch Delete | POST | `/api/{entity}/batch/delete` |
| Batch Edit | PATCH | `/api/{entity}/batch/edit` |
| Batch Create | POST | `/api/{entity}/batch/new` |

## Entity Domains

The CLI supports 26+ entity domains:

- **contacts** — Marketing contacts/leads
- **campaigns** — Marketing campaigns
- **emails** — Email templates
- **forms** — Web forms
- **segments** — Contact segments/lists
- **users** — Mautic users
- **assets** — Downloadable assets
- **categories** — Item categories
- **companies** — Company records
- **devices** — Contact devices
- **dynamiccontents** — Dynamic content blocks
- **fields** — Custom fields
- **files** — Media files
- **hooks** — Webhooks
- **messages** — Automated messages
- **notes** — Contact notes
- **notifications** — System notifications
- **pages** — Landing pages
- **points** — Point actions
- **reports** — Analytics reports
- **smses** — SMS templates
- **stages** — Lifecycle stages
- **tags** — Item tags
- **tweets** — Social tweets
- **points/triggers** — Point trigger events

## State Model

- **Project config** (`.mautic_project.json`): Stores instance URL, API credentials
- **Session state** (`.mautic_session.json`): Tracks current entity, current item, history
- **Entity cache** (`.mautic_entities/`): Cached list results for offline inspection

## Key Patterns

1. **Always authenticate first**: `cli-anything-mautic config set --base-url <url> --api-key-id <id> --api-key-secret <secret>`
2. **Use `--json` for agent consumption**: Every command supports `--json` flag
3. **Batch operations**: Use `batch --op delete/edit/update/create --data '{"ids": [1,2,3]}'`
4. **Cross-entity operations**: Add contacts to campaigns/segments, send emails to contacts

## Common Workflows

### Manage Contacts
```bash
cli-anything-mautic contacts list --limit 10
cli-anything-mautic contacts create --data '{"email": "test@example.com", "firstname": "Test"}'
cli-anything-mautic contacts edit 1 --data '{"firstname": "Updated"}'
cli-anything-mautic contacts delete 1
```

### Manage Campaigns
```bash
cli-anything-mautic campaigns list
cli-anything-mautic campaigns create --data '{"name": "My Campaign", "color": "#3375C5"}'
cli-anything-mautic campaigns add-contact 1 --contact-id 5
```

### Export Data
```bash
cli-anything-mautic export entities contacts --format json --limit 100
cli-anything-mautic export entities contacts --format csv
```
