import platform
import subprocess
from pathlib import Path

import typer

from app.file_creation_commands import (
    create_pre_commit_config,
    create_project_structure,
    create_tox_ini,
    delete_project_files,
    install_poetry,
)
from app.helper import check_file_exists, find_pyproject_toml, is_poetry_installed

app = typer.Typer()


@app.command()
def new(
    project_name: str,
    default: bool = typer.Option(False, help="Use default settings"),
    fastapi: bool = typer.Option(False, help="Create a minimal FastAPI app in main.py"),
):
    python_version = (
        "3.10" if default else typer.prompt("Enter the Python version", type=str)
    )
    author_name = (
        "John Doe" if default else typer.prompt("Enter the author's name", type=str)
    )

    create_project_structure(project_name, python_version, author_name, fastapi)
    project_dir = Path.cwd()
    create_tox_ini(project_dir)
    create_pre_commit_config(project_dir)
    typer.echo(
        f"'src/{project_name}' project structure created with Python version {python_version}."
    )


@app.command()
def check_files(project_name: str, fastapi: bool = False):
    base_dir = Path.cwd()
    paths_to_check = [
        base_dir / "pyproject.toml",
        base_dir / ".pre-commit-config.yaml",
        base_dir / "tox.ini",
        base_dir / "README.md",
        base_dir / "LICENSE.md",
        base_dir / "src",
        base_dir / "tests",
        base_dir / "src" / project_name,
    ]
    if fastapi:
        paths_to_check.append(base_dir / "src" / project_name / "main.py")
    for path in paths_to_check:
        check_file_exists(path)


@app.command()
def delete_all(project_name: str, fastapi: bool = False):
    """Deletes all files and directories associated with the project."""
    if typer.confirm(
        f"Are you sure you want to delete all files for '{project_name}'? This action cannot be undone."
    ):
        delete_project_files(project_name, fastapi)
        typer.echo("Deletion completed.")
    else:
        typer.echo("Deletion cancelled.")


@app.command()
def setup_poetry():
    """Check for Poetry installation and install if not present."""
    if is_poetry_installed():
        typer.echo("Poetry is already installed.")
    else:
        typer.echo("Poetry is not installed.")
        if typer.confirm("Do you want to install Poetry now?"):
            install_poetry()
        else:
            typer.echo("Poetry installation skipped.")


@app.command()
def create_venv():
    """Create a virtual environment named '.venv' and configure Poetry for local virtualenv creation."""
    try:
        subprocess.run(
            ["poetry", "config", "virtualenvs.create", "true", "--local"], check=True
        )
        typer.echo("Configured Poetry to create virtual environments locally.")
        subprocess.run(["python", "-m", "venv", ".venv"], check=True)
        typer.echo("Virtual environment '.venv' created successfully.")
    except subprocess.CalledProcessError as e:
        typer.echo(f"Failed to execute command: {e}")


@app.command()
def use_venv():
    """Switch to using the '.venv' environment with Poetry."""
    cwd = Path.cwd()
    if not find_pyproject_toml(cwd):
        typer.echo(
            "Poetry could not find a pyproject.toml file in the current or parent directories."
        )
        raise typer.Exit()
    venv_path = cwd / ".venv" / "bin" / "python"
    if platform.system() == "Windows":
        venv_path = cwd / ".venv" / "Scripts" / "python.exe"
    if not venv_path.exists():
        typer.echo(
            "Virtual environment '.venv' does not exist. Please create it first."
        )
        raise typer.Exit()
    try:
        subprocess.run(["poetry", "env", "use", str(venv_path)], check=True)
        typer.echo("Switched to virtual environment '.venv'.")
    except subprocess.CalledProcessError as e:
        typer.echo(f"Failed to switch to virtual environment: {e}")


if __name__ == "__main__":
    app()
