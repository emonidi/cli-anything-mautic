"""cli-anything — meta CLI for discovering and managing CLI-Anything tools."""

import glob
import json
import os
import re
import shutil
import sys
from pathlib import Path

import click


def _extract_version_from_setup(setup_path: str) -> str | None:
     """Extract version from a setup.py file using regex."""
    try:
        content = Path(setup_path).read_text()
        match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
        return match.group(1) if match else None
    except Exception:
        return None


def _find_installed_tools() -> dict:
     """Scan installed cli-anything-* packages via importlib.metadata."""
    installed = {}
    try:
        from importlib.metadata import distributions

        for dist in distributions():
            name = dist.metadata.get("Name", "")
            if not name.startswith("cli-anything-"):
                continue
            software = name.replace("cli-anything-", "")
            version = dist.version

             # Try to find the executable
            exe_name = f"cli-anything-{software}"
            executable = shutil.which(exe_name)

             # Try to find source path from package location
            source = None
            try:
                loc = dist.files   # list of PathLike objects
                for f in loc:
                    fp = str(f)
                    if "agent-harness" in fp and "__init__.py" in fp:
                        p = Path(fp)
                        ah_idx = None
                        parts = p.parts
                        for i, part in enumerate(parts):
                            if part == "agent-harness" and i + 1 < len(parts):
                                if parts[i + 1] == "cli_anything":
                                    ah_idx = i
                                    break
                        if ah_idx is not None:
                            source = str(Path(*parts[:ah_idx + 2]))
                            break
            except Exception:
                pass

            installed[software] = {
                 "status": "installed",
                 "version": version,
                 "executable": executable,
                 "source": source,
             }
    except Exception:
        pass
    return installed


def _find_generated_tools(base_path: str, max_depth: int | None) -> dict:
     """Scan for locally generated CLI-Anything tools via glob patterns."""
    generated = {}
    base = Path(base_path).resolve()
    suffix = "agent-harness/cli_anything/*/__init__.py"

    def build_glob_patterns(b: Path, depth: int | None) -> list[str]:
        if depth is None:
            return [str(b / "**" / suffix)]
        patterns: list[str] = []
        for d in range(depth + 1):
            if d == 0:
                patterns.append(str(b / suffix))
            else:
                prefix = "/".join(["*"] * d)
                patterns.append(str(b / prefix / suffix))
        return patterns

    try:
        patterns = build_glob_patterns(base, max_depth)
        seen = set()
        for pattern in patterns:
            for init_file in glob.glob(pattern, recursive=True):
                if init_file in seen:
                    continue
                seen.add(init_file)
                parts = Path(init_file).parts
                ah_idx = None
                for i, p in enumerate(parts):
                    if p == "cli_anything" and i + 1 < len(parts):
                        ah_idx = i
                        break
                if ah_idx is None:
                    continue
                software = parts[ah_idx + 1]
                 # Find agent-harness index
                ah_found = None
                for i, p in enumerate(parts):
                    if p == "agent-harness":
                        ah_found = i
                        break
                if ah_found is None:
                    ah_found = ah_idx - 1
                source = str(Path(*parts[:ah_found + 2]))
                setup_path = str(Path(*parts[:ah_found + 1]) / "setup.py")
                version = _extract_version_from_setup(setup_path)
                generated[software] = {
                     "status": "generated",
                     "version": version,
                     "executable": None,
                     "source": source,
                 }
    except Exception:
        pass
    return generated


def _merge_results(installed: dict, generated: dict) -> list[dict]:
     """Merge installed and generated results, preferring installed data."""
    merged: dict[str, dict] = {}
    for name, data in installed.items():
        merged[name] = dict(data)
    for name, data in generated.items():
        if name not in merged:
            merged[name] = dict(data)
        else:
             # Both exist — keep installed, add source from generated if missing
            if not merged[name].get("source") and data.get("source"):
                merged[name]["source"] = data["source"]
    return sorted(merged.values(), key=lambda x: x["name"])


@click.group()
def cli():
     """cli-anything — meta CLI for discovering and managing CLI-Anything tools."""
    pass


@cli.command()
@click.option("--path", "search_path", default=None, help="Directory to search for CLI-Anything tools (default: current directory)")
@click.option("--depth", "max_depth", default=None, type=int, help="Maximum recursion depth (0=current dir only, None=unlimited)")
@click.option("--json", "as_json", is_flag=True, help="Output in JSON format")
def list(search_path: str | None, max_depth: int | None, as_json: bool):
     """List all available CLI-Anything tools (installed and generated).

    Scans for cli-anything-* packages (via importlib.metadata) and
    locally generated tools (via glob patterns in agent-harness/ directories).
     """
     # Validate path
    base = Path(search_path or ".").resolve()
    if not base.is_dir():
        click.echo(f"Error: Path not found: {search_path}", err=True)
        sys.exit(1)

     # Scan
    installed = _find_installed_tools()
    generated = _find_generated_tools(str(base), max_depth)
    tools = _merge_results(installed, generated)

     # Count stats
    total = len(tools)
    n_installed = sum(1 for t in tools if t["status"] == "installed")
    n_generated = total - n_installed

    if as_json:
        click.echo(json.dumps({
             "tools": tools,
             "total": total,
             "installed": n_installed,
             "generated_only": n_generated,
         }, indent=2))
        return

    if not tools:
        click.echo("No CLI-Anything tools found.")
        return

    click.echo(f"CLI-Anything Tools (found {total})\n")

     # Build table
    header = f"{'Name':<16} {'Status':<12} {'Version':<10} {'Source'}"
    click.echo(header)
    click.echo("-" * len(header))
    for t in tools:
        name = t["name"]
        status = t["status"]
        version = t.get("version") or "?"
        source = t.get("source") or ""
        click.echo(f"{name:<16} {status:<12} {version:<10} {source}")


cli.add_command(list, "list")


if __name__ == "__main__":
    cli()
