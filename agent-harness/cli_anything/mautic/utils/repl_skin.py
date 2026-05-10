"""Unified REPL skin — branded interactive prompt for Mautic CLI."""

import os
import sys
from typing import Any, Dict, List, Optional

try:
    from prompt_toolkit import HTML, print_formatted_text
    from prompt_toolkit.styles import Style
    from prompt_toolkit.session import Session
    HAS_PROMPT_TOOLKIT = True
except ImportError:
    HAS_PROMPT_TOOLKIT = False


class ReplSkin:
    """Branded REPL interface for the Mautic CLI."""

    def __init__(self, name: str = "mautic", version: str = "1.0.0"):
        self.name = name
        self.version = version
        self._skill_path = self._find_skill_path()

    def _find_skill_path(self) -> Optional[str]:
        """Find the SKILL.md path inside the package directory."""
        # Check if skills/SKILL.md exists in this package's directory
        package_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        skill_path = os.path.join(package_dir, "skills", "SKILL.md")
        if os.path.exists(skill_path):
            return skill_path
        # Also check from current working directory
        for root in [os.getcwd(), os.path.expanduser("~")]:
            candidate = os.path.join(root, "skills", f"cli-anything-{self.name}", "SKILL.md")
            if os.path.exists(candidate):
                return candidate
        return None

    def print_banner(self) -> None:
        """Print the branded startup banner."""
        banner = f"""
  \033[1;36m{'=' * 50}\033[0m
  \033[1;33m{self.name.upper()} CLI\033[0m  v{self.version}
  \033[1;36mPython Mautic API Harness\033[0m
  \033[1;36m{'=' * 50}\033[0m
"""
        print(banner)
        if self._skill_path:
            print(f"  \033[1mSkill:\033[0m {self._skill_path}")
            print("  Type \033[1;33mhelp skill\033[0m to read the skill definition.")
        print()
        print("  Type \033[1;33mhelp\033[0m for commands, \033[1;33mexit\033[0m to quit.")
        print()

    def print_goodbye(self) -> None:
        """Print the branded exit message."""
        print(f"  \033[1;32mGoodbye!\033[0m  ({self.name} CLI v{self.version})")
        print()

    def create_prompt_session(self) -> Any:
        """Create a prompt_toolkit session with history and styling."""
        if not HAS_PROMPT_TOOLKIT:
            return None
        style = Style.from_dict({
            "prompt": "ansiblue bold",
            "logo": "ansiyellow bold",
        })
        session = Session(
            history_filename=os.path.expanduser(f"~/.cache/{self.name}/history"),
            style=style,
        )
        return session

    def get_input(self, session: Any = None, project_name: str = "",
                  modified: bool = False) -> str:
        """Get user input with branded prompt."""
        if not HAS_PROMPT_TOOLKIT:
            return input(f"({self.name} {project_name}{' *' if modified else ''})> ")
        prompt_str = f"({self.name} {project_name}{' *' if modified else ''})> "
        return input(prompt_str)

    def success(self, msg: str) -> None:
        """Print success message."""
        print(f"  \033[1;32m✓ {msg}\033[0m")

    def error(self, msg: str) -> None:
        """Print error message."""
        print(f"  \033[1;31m✗ {msg}\033[0m")

    def warning(self, msg: str) -> None:
        """Print warning message."""
        print(f"  \033[1;33m⚠ {msg}\033[0m")

    def info(self, msg: str) -> None:
        """Print info message."""
        print(f"  \033[1;34m● {msg}\033[0m")

    def status(self, key: str, value: str) -> None:
        """Print key-value status line."""
        print(f"  \033[1m{key}:\033[0m {value}")

    def table(self, headers: List[str], rows: List[List[str]],
              col_widths: Optional[List[int]] = None) -> None:
        """Print formatted table."""
        if not rows:
            print("  (no data)")
            return
        if col_widths is None:
            all_rows = [headers] + rows
            col_widths = [max(len(str(cell)) for cell in col) for col in zip(*all_rows)]
        header_line = "  | ".join(h.ljust(w) for h, w in zip(headers, col_widths))
        print("  " + "-" * len(header_line.strip()))
        print(header_line)
        print("  " + "-" * len(header_line.strip()))
        for row in rows:
            print("  | ".join(str(c).ljust(w) for c, w in zip(row, col_widths)))
        print("  " + "-" * len(header_line.strip()))

    def help(self, commands: Dict[str, str]) -> None:
        """Print formatted help listing."""
        print()
        print("  \033[1mCommands:\033[0m")
        for name, desc in sorted(commands.items()):
            print(f"    \033[1m{name}\033[0m  {desc}")
        print()

    def progress(self, current: int, total: int, label: str = "") -> None:
        """Print progress bar."""
        pct = current / total if total > 0 else 0
        filled = int(pct * 30)
        bar = "▓" * filled + "░" * (30 - filled)
        print(f"  [{bar}] {current}/{total} {label}")

    def print_result(self, data: Any, as_json: bool = False) -> None:
        """Print result data, formatted."""
        if as_json:
            import json
            print(json.dumps(data, indent=2, default=str))
        elif isinstance(data, dict):
            for k, v in data.items():
                print(f"  \033[1m{k}:\033[0m {v}")
        elif isinstance(data, list):
            for item in data:
                print(f"  {item}")
        else:
            print(f"  {data}")
