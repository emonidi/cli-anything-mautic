"""cli-anything-mautic — CLI harness for the Mautic API.

A stateful CLI that wraps the Mautic REST API, providing both one-shot commands
and an interactive REPL mode. Uses direct HTTP calls to the Mautic instance
(authenticated via API key).
"""

import json
import os
import sys
from typing import Any, Dict, List, Optional

import click
from click.core import Context

# Ensure package is importable
_parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _parent not in sys.path:
    sys.path.insert(0, _parent)

from cli_anything.mautic.core.project import (
    load_project, save_project, load_session, save_session,
    has_credentials, get_entity_dir, clear_entity_cache,
    save_entity_cache, load_entity_cache,
)
from cli_anything.mautic.utils.api_client import MauticClient
from cli_anything.mautic.utils.helpers import get_client
from cli_anything.mautic.utils.repl_skin import ReplSkin

VERSION = "1.0.0"
CLI_NAME = "cli-anything-mautic"


def _json_flag(f):
    """Add --json flag to a command."""
    return click.option("--json", "as_json", is_flag=True, help="Output as JSON")(f)


def _entity_dir_ctx(ctx):
    """Get project path from context."""
    p = ctx.ensure_object(dict).get("_project_path")
    return p or os.getcwd()


# ─── Config Commands ───────────────────────────────────────────────────────────

@click.group()
@click.option("--project", "_project_path", hidden=True, default=None)
@click.pass_context
def cli(ctx, _project_path):
    """cli-anything-mautic — Stateful CLI harness for the Mautic API.

    A Python CLI that wraps the Mautic REST API, providing both one-shot
    commands and an interactive REPL mode. Uses direct HTTP calls to your
    Mautic instance (authenticated via API key).
    """
    ctx.ensure_object(dict)
    ctx.obj["_project_path"] = _project_path
    if ctx.invoked_subcommand is None:
        from cli_anything.mautic.mautic_cli import repl
        ctx.invoke(repl)


@cli.group()
@click.pass_context
def config(ctx):
    """Manage Mautic instance configuration."""
    ctx.ensure_object(dict)


@config.command(name="show")
@click.pass_context
def config_show(ctx):
    """Show current configuration."""
    proj = load_project(_entity_dir_ctx(ctx))
    click.echo(json.dumps(proj, indent=2))

@config.command(name="set")
@click.option("--base-url", help="Mautic base URL (e.g., https://mycompany.com/mautic)")
@click.option("--api-key-id", help="API Key ID")
@click.option("--api-key-secret", help="API Key Secret")
@click.option("--oauth2-token-endpoint", help="OAuth2 token endpoint URL")
@click.pass_context
def config_set(ctx, base_url, api_key_id, api_key_secret, oauth2_token_endpoint):
    """Set configuration values."""
    kwargs = {}
    if base_url:
        kwargs["base_url"] = base_url
    if api_key_id:
        kwargs["api_key_id"] = api_key_id
    if api_key_secret:
        kwargs["api_key_secret"] = api_key_secret
    if oauth2_token_endpoint:
        kwargs["oauth2_token_endpoint"] = oauth2_token_endpoint
    if kwargs:
        save_project(_entity_dir_ctx(ctx), **kwargs)
        click.echo("  Saved configuration.")
    else:
        click.echo("  Nothing to set. Provide at least one option.")


@config.command(name="unset")
@click.option("--base-url", is_flag=True, help="Clear base URL")
@click.option("--api-key-id", is_flag=True, help="Clear API Key ID")
@click.option("--api-key-secret", is_flag=True, help="Clear API Key Secret")
@click.pass_context
def config_unset(ctx, base_url, api_key_id, api_key_secret):
    """Clear configuration values."""
    kwargs = {}
    if base_url:
        kwargs["base_url"] = ""
    if api_key_id:
        kwargs["api_key_id"] = ""
    if api_key_secret:
        kwargs["api_key_secret"] = ""
    if kwargs:
        save_project(_entity_dir_ctx(ctx), **kwargs)
        click.echo("  Cleared configuration.")
    else:
        click.echo("  Nothing to unset.")


# ─── Project Commands ──────────────────────────────────────────────────────────

@cli.group()
@click.pass_context
def project(ctx):
    """Manage project directory."""
    ctx.ensure_object(dict)


@project.command(name="init")
@click.pass_context
def project_init(ctx):
    """Initialize a new Mautic project."""
    target = _entity_dir_ctx(ctx)
    save_project(target)
    click.echo(f"  Project initialized in {target}/")
    click.echo(f"  Run: cd {target}")
    click.echo(f"  Then: cli-anything-mautic config set --base-url <url>")


# ─── Generic Entity Commands ───────────────────────────────────────────────────

def _make_entity_group(entity_name, display_name=""):
    """Create a Click group for an entity with standard CRUD commands."""
    if not display_name:
        display_name = entity_name.title()

    @click.group(entity_name, help=f"{display_name} operations")
    @click.pass_context
    def group(ctx):
        ctx.ensure_object(dict)

    # list
    @group.command("list")
    @click.option("--limit", "-l", default=10, help="Max results")
    @click.option("--offset", "-O", default=0, help="Result offset")
    @click.option("--filter", "-f", "filters", multiple=True, help="Filter key=value")
    @_json_flag
    @click.pass_context
    def list_cmd(ctx, limit, offset, filters, as_json):
        """List {name} entities."""
        try:
            client = get_client(_entity_dir_ctx(ctx))
            params = {"limit": limit, "offset": offset}
            for f in filters:
                if "=" in f:
                    k, v = f.split("=", 1)
                    params[k] = v
            result = client.list(entity_name, **params)
            items = result.get(entity_name, result.get("list", result.get("entities", [])))
            if isinstance(items, dict):
                items = list(items.values())
            if as_json:
                click.echo(json.dumps({"total": result.get("total", len(items)), "items": items}, indent=2, default=str))
            else:
                click.echo(f"  Total: {result.get('total', len(items))}")
                for item in items[:20]:
                    ident = item.get("id", item.get("name", item.get("email", "?")))
                    name = item.get("name", item.get("email", ""))
                    click.echo(f"     {item.get('id', '?'):>6}   {name}")
                if len(items) > 20:
                    click.echo(f"      ... and {len(items) - 20} more")
        except Exception as e:
            click.echo(f"   \033[1;31mError: {e}\033[0m", err=True)
            sys.exit(1)

    # get
    @group.command()
    @click.argument("id", type=int)
    @_json_flag
    @click.pass_context
    def get_cmd(ctx, id, as_json):
        """Get a single {name} by ID."""
        try:
            client = get_client(_entity_dir_ctx(ctx))
            result = client.get(entity_name, id)
            click.echo(json.dumps(result, indent=2, default=str))
        except Exception as e:
            click.echo(f"    [1;31mError: {e}[0m", err=True)
            save_session(_entity_dir_ctx(ctx), current_entity=entity_name, current_item=id)
            sys.exit(1)
        save_session(_entity_dir_ctx(ctx), current_entity=entity_name, current_item=id)
    @group.command()
    @click.option("--data", "-d", "data_json", help="JSON data string")
    @click.option("--file", "-f", "data_file", help="JSON data file")
    @_json_flag
    @click.pass_context
    def create(ctx, data_json, data_file, as_json):
        """Create a new {name}."""
        try:
            data = {}
            if data_json:
                data = json.loads(data_json)
            elif data_file:
                with open(data_file) as fh:
                    data = json.load(fh)
            else:
                click.echo("  Provide --data or --file with JSON.")
                return
            client = get_client(_entity_dir_ctx(ctx))
            result = client.create(entity_name, data)
            if as_json:
                click.echo(json.dumps(result, indent=2, default=str))
            else:
                click.echo(f"  Created {entity_name} #{result.get('id', '?')}")
        except Exception as e:
            click.echo(f"   \033[1;31mError: {e}\033[0m", err=True)
            sys.exit(1)

    # edit
    @group.command()
    @click.argument("id", type=int)
    @click.option("--data", "-d", "data_json", help="JSON data string")
    @click.option("--file", "-f", "data_file", help="JSON data file")
    @click.option("--strict", is_flag=True, help="Strict mode")
    @click.option("--ignore-missing", is_flag=True, help="Ignore missing fields")
    @_json_flag
    @click.pass_context
    def edit(ctx, id, data_json, data_file, strict, ignore_missing, as_json):
        """Edit an existing {name}."""
        try:
            data = {}
            if data_json:
                data = json.loads(data_json)
            elif data_file:
                with open(data_file) as fh:
                    data = json.load(fh)
            else:
                click.echo("  Provide --data or --file with JSON.")
                return
            client = get_client(_entity_dir_ctx(ctx))
            result = client.edit(entity_name, id, data, strict, ignore_missing)
            if as_json:
                click.echo(json.dumps(result, indent=2, default=str))
            else:
                click.echo(f"  Updated {entity_name} #{id}")
        except Exception as e:
            click.echo(f"   \033[1;31mError: {e}\033[0m", err=True)
            sys.exit(1)

    # update
    @group.command()
    @click.argument("id", type=int)
    @click.option("--data", "-d", "data_json", help="JSON data string")
    @click.option("--file", "-f", "data_file", help="JSON data file")
    @_json_flag
    @click.pass_context
    def update(ctx, id, data_json, data_file, as_json):
        """Update {name} (create if not exists)."""
        try:
            data = {}
            if data_json:
                data = json.loads(data_json)
            elif data_file:
                with open(data_file) as fh:
                    data = json.load(fh)
            else:
                click.echo("  Provide --data or --file with JSON.")
                return
            client = get_client(_entity_dir_ctx(ctx))
            result = client.update(entity_name, id, data)
            if as_json:
                click.echo(json.dumps(result, indent=2, default=str))
            else:
                click.echo(f"   {'Created' if 'id' not in str(result.get('', {})) else 'Updated'} {entity_name} #{id}")
        except Exception as e:
            click.echo(f"   \033[1;31mError: {e}\033[0m", err=True)
            sys.exit(1)

    # delete
    @group.command()
    @click.argument("id", type=int)
    @_json_flag
    @click.pass_context
    def delete(ctx, id, as_json):
        """Delete a {name}."""
        try:
            client = get_client(_entity_dir_ctx(ctx))
            result = client.delete(entity_name, id)
            if as_json:
                click.echo(json.dumps(result, indent=2, default=str))
            else:
                click.echo(f"  Deleted {entity_name} #{id}")
        except Exception as e:
            click.echo(f"   \033[1;31mError: {e}\033[0m", err=True)
            sys.exit(1)

    # batch
    @group.command()
    @click.option("--data", "-d", "data_json", help="JSON data string")
    @click.option("--file", "-f", "data_file", help="JSON data file")
    @click.option("--op", "-o", "operation", type=click.Choice(["delete", "edit", "update", "create"]),
                   help="Batch operation type")
    @_json_flag
    @click.pass_context
    def batch(ctx, data_json, data_file, operation, as_json):
        """Batch operations on {name}."""
        try:
            data = {}
            if data_json:
                data = json.loads(data_json)
            elif data_file:
                with open(data_file) as fh:
                    data = json.load(fh)
            else:
                click.echo("  Provide --data or --file with JSON.")
                return
            client = get_client(_entity_dir_ctx(ctx))
            op = operation or "edit"
            if op == "delete":
                result = client.batch_delete(entity_name, data.get("ids", []))
            elif op == "create":
                result = client.batch_create(entity_name, data.get("batch", []))
            elif op == "update":
                result = client.batch_update(entity_name, data)
            else:
                result = client.batch_edit(entity_name, data)
            if as_json:
                click.echo(json.dumps(result, indent=2, default=str))
            else:
                click.echo(f"  Batch {op} on {entity_name}: {result.get('success', '?')} succeeded")
        except Exception as e:
            click.echo(f"   \033[1;31mError: {e}\033[0m", err=True)
            sys.exit(1)

    # Fix docstrings to use actual entity name
    dn = display_name or entity_name.title()
    for _cn, cmd in group.commands.items():
        if cmd.__doc__:
            cmd.__doc__ = cmd.__doc__.format(name=dn)
            cmd.help = cmd.__doc__

    return group


# ─── Helper Commands ────────────────────────────────────────────────────────────

@cli.group()
@click.pass_context
def cache(ctx):
    """Manage entity cache."""
    ctx.ensure_object(dict)


@cache.command(name="clear")
@click.argument("entity", required=False)
@click.pass_context
def cache_clear(ctx, entity):
    """Clear entity cache."""
    clear_entity_cache(_entity_dir_ctx(ctx), entity)
    if entity:
        click.echo(f"  Cleared cache for: {entity}")
    else:
        click.echo("  Cleared all entity caches.")


@cache.command(name="list")
@click.pass_context
def cache_list(ctx):
    """List cached entities."""
    dir_path = get_entity_dir(_entity_dir_ctx(ctx))
    if os.path.exists(dir_path):
        for f in sorted(os.listdir(dir_path)):
            if f.endswith(".json"):
                click.echo(f"     {f}")
    else:
        click.echo("  No cache directory yet.")


@cli.group()
@click.pass_context
def export(ctx):
    """Export entity data."""
    ctx.ensure_object(dict)


@export.command(name="entities")
@click.argument("entity")
@click.option("--format", "-f", "fmt", type=click.Choice(["json", "csv"]), default="json")
@click.option("--pretty", is_flag=True, default=True, help="Pretty print JSON")
@click.option("--limit", "-l", default=100, help="Max items")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
@click.pass_context
def export_entities(ctx, entity, fmt, pretty, limit, as_json):
    """Export all entities of a type."""
    try:
        client = get_client(_entity_dir_ctx(ctx))
        result = client.list(entity, limit=limit)
        items = result.get(entity, result.get("list", []))
        from cli_anything.mautic.core.export import export_entity
        output = export_entity(entity, items, fmt, pretty)
        click.echo(output)
    except Exception as e:
        click.echo(f"   \033[1;31mError: {e}\033[0m", err=True)
        sys.exit(1)


# ─── REPL ───────────────────────────────────────────────────────────────────────

_REPL_COMMANDS = {
      "config": "Manage Mautic instance configuration",
      "project": "Manage project directory",
      "cache": "Manage entity cache",
      "export": "Export entity data",
      "contacts": "Contact operations (list, get, create, edit, delete, batch)",
      "campaigns": "Campaign operations",
      "emails": "Email operations",
      "forms": "Form operations",
      "segments": "Segment operations",
      "users": "User operations",
      "help": "Show help",
      "exit": "Exit REPL",
}


def _build_commands_dict():
    return dict(_REPL_COMMANDS)


def repl():
    """Interactive REPL for Mautic CLI."""
    skin = ReplSkin("mautic", VERSION)
    skin.print_banner()

    project_path = os.getcwd()
    proj = load_project(project_path)
    project_name = proj.get("base_url", "").split("/")[-1] or "untitled"

    session = skin.create_prompt_session()
    modified = False

    while True:
        try:
            line = skin.get_input(session, project_name, modified)
        except (EOFError, KeyboardInterrupt):
            skin.print_goodbye()
            break

        line = line.strip()
        if not line:
            continue

        if line in ("exit", "quit", "q", "bye"):
            skin.print_goodbye()
            break

        if line == "help":
            skin.help(_build_commands_dict())
            continue

        if line == "help skill" and skin._skill_path:
            try:
                with open(skin._skill_path) as f:
                    click.echo(f.read())
            except FileNotFoundError:
                skin.warning("Skill file not found.")
            continue

        try:
            from click.testing import CliRunner
            runner = CliRunner(mix_stderr=False)
            result = runner.invoke(cli, line.split(), catch_exceptions=False)
            if result.stdout:
                click.echo(result.stdout, nl=False)
            if result.stderr:
                click.echo(result.stderr, nl=False, err=True)
            if result.exception and not (result.stdout or result.stderr):
                skin.error(str(result.exception))
        except Exception as e:
            skin.error(str(e))


# ─── Register Dynamic Entity Groups ─────────────────────────────────────────────

_ENTITY_DEFS = [
      ("contacts", "Contacts"),
      ("campaigns", "Campaigns"),
      ("emails", "Emails"),
      ("forms", "Forms"),
      ("segments", "Segments"),
      ("users", "Users"),
      ("assets", "Assets"),
      ("categories", "Categories"),
      ("companies", "Companies"),
      ("devices", "Devices"),
      ("dynamiccontents", "Dynamic Contents"),
      ("fields", "Fields"),
      ("files", "Files"),
      ("hooks", "Hooks"),
      ("messages", "Messages"),
      ("notes", "Notes"),
      ("notifications", "Notifications"),
      ("pages", "Pages"),
      ("points", "Points"),
      ("reports", "Reports"),
      ("smses", "SMS"),
      ("stages", "Stages"),
      ("tags", "Tags"),
      ("themes", "Themes"),
      ("tweets", "Tweets"),
]

for name, display in _ENTITY_DEFS:
    group = _make_entity_group(name, display)
    cli.add_command(group, name)


# ─── Main Entry Point ───────────────────────────────────────────────────────────

def main():
    """CLI entry point."""
    cli(standalone_mode=False)


if __name__ == "__main__":
    main()
