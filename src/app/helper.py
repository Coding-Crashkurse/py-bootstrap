from pathlib import Path
import subprocess
import typer
from colorama import Fore, Style
import re


def find_pyproject_toml(start_path: Path) -> bool:
    """Check if a pyproject.toml file exists in the current or parent directories."""
    current_path = start_path
    while current_path != current_path.parent:
        if (current_path / "pyproject.toml").exists():
            return True
        current_path = current_path.parent


def is_poetry_installed() -> bool:
    """Check if Poetry is installed."""
    try:
        subprocess.run(
            ["poetry", "--version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def check_file_exists(file_path: Path):
    """Check if a file exists and print a colored message."""
    if file_path.exists():
        typer.echo(Fore.GREEN + "✔ " + Style.RESET_ALL + str(file_path))
    else:
        typer.echo(Fore.RED + "✖ " + Style.RESET_ALL + str(file_path))


def validate_project_name(project_name: str) -> str:
    if not re.match(r"^[a-z_]+$", project_name):
        raise ValueError(
            "Project name must contain only lowercase letters and underscores."
        )
    return project_name


def validate_author_name(author_name: str) -> str:
    if not re.match(r"^[a-zA-Z\s]+$", author_name):
        raise ValueError("Author name must contain only letters and spaces.")
    return author_name
