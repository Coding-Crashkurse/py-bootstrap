# import platform
# import re
# import subprocess
# from datetime import datetime
# from pathlib import Path
#
# import toml
# import typer
# from colorama import Fore, Style, init
#
# app = typer.Typer()
# init()
#
#
# def validate_project_name(project_name: str) -> str:
#     if not re.match(r"^[a-z_]+$", project_name):
#         raise ValueError(
#             "Project name must contain only lowercase letters and underscores."
#         )
#     return project_name
#
#
# def validate_author_name(author_name: str) -> str:
#     if not re.match(r"^[a-zA-Z\s]+$", author_name):
#         raise ValueError("Author name must contain only letters and spaces.")
#     return author_name
#
#
# def create_fastapi_app(app_dir: Path):
#     fastapi_app_content = """from fastapi import FastAPI
#
# app = FastAPI()
#
# @app.get("/")
# def read_root():
#     return {"Hello": "World"}
# """
#     main_py = app_dir / "main.py"
#     main_py.write_text(fastapi_app_content)
#
#
# def create_simple_test(tests_dir: Path):
#     test_content = """def test_example():
#     assert 1 == 1
# """
#     test_file = tests_dir / "test_example.py"
#     test_file.write_text(test_content)
#
#
# def create_license_file(project_dir: Path, author_name: str):
#     current_year = datetime.now().year
#     license_text = f"""MIT License
#
# Copyright (c) {current_year} {author_name}
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# """
#     license_file = project_dir / "LICENSE.md"
#     license_file.write_text(license_text)
#
#
# def create_project_structure(
#     project_name: str, python_version: str, author_name: str, fastapi: bool
# ):
#     project_name = validate_project_name(project_name)
#     author_name = validate_author_name(author_name)
#     project_dir = Path.cwd()
#     src_dir = project_dir / "src"
#     app_dir = src_dir / project_name
#     tests_dir = project_dir / "tests"
#
#     src_dir.mkdir(exist_ok=True)
#     app_dir.mkdir(exist_ok=True)
#     tests_dir.mkdir(exist_ok=True)
#     (app_dir / "__init__.py").touch()
#     (tests_dir / "__init__.py").touch()
#
#     if fastapi:
#         create_fastapi_app(app_dir)
#     create_simple_test(tests_dir)
#     create_license_file(project_dir, author_name)
#
#     pyproject_content = {
#         "build-system": {
#             "requires": ["poetry-core"],
#             "build-backend": "poetry.core.masonry.api",
#         },
#         "tool": {
#             "poetry": {
#                 "name": project_name,
#                 "version": "0.0.1",
#                 "description": "",
#                 "authors": [author_name.strip()],
#                 "readme": "README.md",
#                 "dependencies": {
#                     "python": python_version,
#                     "typer": "^0.9.0",
#                     "toml": "^0.10.2",
#                     "colorama": "^0.4.6",
#                 },
#                 "group": {
#                     "dev": {
#                         "dependencies": {
#                             "isort": "^5.13.2",
#                             "flake8": "^7.0.0",
#                             "black": "^23.12.1",
#                             "tox": "^4.11.4",
#                             "mypy": "^0.910",
#                         }
#                     }
#                 },
#             }
#         },
#     }
#     if fastapi:
#         pyproject_content["tool"]["poetry"]["dependencies"]["fastapi"] = "^0.108.0"
#
#     (Path("pyproject.toml").write_text(toml.dumps(pyproject_content)))
#     (Path("README.md").touch())
#
#     create_tox_ini(project_dir)
#     create_pre_commit_config(project_dir)
#
#
# def create_tox_ini(project_dir: Path):
#     tox_ini_content = """[tox]
# envlist = format,lint,mypy,test,pre-commit
# isolated_build = True
# skipsdist = True
#
# [testenv]
# allowlist_externals = poetry
# basepython = python3
# skip_install = true
# commands_pre = poetry install
#
# [testenv:format]
# commands = poetry run black src tests
#             poetry run isort src tests
#
# [testenv:lint]
# commands = poetry run flake8 src tests
#             poetry run black --check src tests
#             poetry run isort --check-only src tests
#
# [testenv:mypy]
# commands = poetry run mypy src tests
#
# [testenv:test]
# commands = poetry run pytest
#
# [flake8]
# max-line-length = 88
# select = C,E,F,W,B,B9
# ignore = E501, E902, W503, W291
# exclude = __init__.py
# """
#     tox_ini_path = project_dir / "tox.ini"
#     tox_ini_path.write_text(tox_ini_content)
#
#
# def create_mypy_config(project_dir: Path):
#     """Create a mypy.ini configuration file."""
#     mypy_config_content = """[mypy]
# ignore_missing_imports = True
# check_untyped_defs = True
# disallow_untyped_defs = True
# """
#     mypy_config_file = project_dir / "mypy.ini"
#     mypy_config_file.write_text(mypy_config_content)
#
#
# def create_pre_commit_config(project_dir: Path):
#     pre_commit_content = """repos:
# -   repo: https://github.com/pre-commit/pre-commit-hooks
#     rev: v3.4.0
#     hooks:
#     -   id: trailing-whitespace
#     -   id: end-of-file-fixer
#     -   id: check-yaml
#     # ... (add more hooks as needed)
# """
#     pre_commit_config_path = project_dir / ".pre-commit-config.yaml"
#     pre_commit_config_path.write_text(pre_commit_content)
#
#
# def check_file_exists(file_path: Path):
#     """Check if a file exists and print a colored message."""
#     if file_path.exists():
#         typer.echo(Fore.GREEN + "✔ " + Style.RESET_ALL + str(file_path))
#     else:
#         typer.echo(Fore.RED + "✖ " + Style.RESET_ALL + str(file_path))
#
#
# def delete_project_files(project_name: str, fastapi: bool):
#     """Deletes all project files and directories."""
#     base_dir = Path.cwd()
#     paths_to_delete = [
#         base_dir / "pyproject.toml",
#         base_dir / "poetry.toml",
#         base_dir / "poetry.lock",
#         base_dir / ".pre-commit-config.yaml",
#         base_dir / "tox.ini",
#         base_dir / "README.md",
#         base_dir / "LICENSE.md",
#         base_dir / "tests",
#         base_dir / "src" / project_name,
#     ]
#
#     if fastapi:
#         paths_to_delete.append(base_dir / "src" / project_name / "main.py")
#
#     for path in paths_to_delete:
#         if path.is_file():
#             path.unlink()
#         elif path.is_dir():
#             for child in path.rglob("*"):
#                 if child.is_file():
#                     child.unlink()
#             path.rmdir()
#
#     src_dir = base_dir / "src"
#     if src_dir.is_dir() and not any(src_dir.iterdir()):
#         src_dir.rmdir()
#     if base_dir.is_dir() and not any(base_dir.iterdir()):
#         base_dir.rmdir()
#
#     typer.echo(f"All files and directories for '{project_name}' have been deleted.")
#
#
# def is_poetry_installed() -> bool:
#     """Check if Poetry is installed."""
#     try:
#         subprocess.run(
#             ["poetry", "--version"],
#             check=True,
#             stdout=subprocess.DEVNULL,
#             stderr=subprocess.DEVNULL,
#         )
#         return True
#     except subprocess.CalledProcessError:
#         return False
#
#
# def find_pyproject_toml(start_path: Path) -> bool:
#     """Check if a pyproject.toml file exists in the current or parent directories."""
#     current_path = start_path
#     while current_path != current_path.parent:
#         if (current_path / "pyproject.toml").exists():
#             return True
#         current_path = current_path.parent
#
#
# @app.command()
# def new(
#     project_name: str,
#     default: bool = typer.Option(False, help="Use default settings"),
#     fastapi: bool = typer.Option(False, help="Create a minimal FastAPI app in main.py"),
# ):
#     """Create a project structure for a professional project"""
#     python_version = (
#         "3.11" if default else typer.prompt("Enter the Python version", type=str)
#     )
#     author_name = (
#         "John Doe" if default else typer.prompt("Enter the author's name", type=str)
#     )
#
#     create_project_structure(project_name, python_version, author_name, fastapi)
#     project_dir = Path.cwd()
#     create_tox_ini(project_dir)
#     create_pre_commit_config(project_dir)
#     typer.echo(
#         f"'src/{project_name}' project structure created with Python version {python_version}."
#     )
#
#
# @app.command()
# def check_files(project_name: str, fastapi: bool = False):
#     base_dir = Path.cwd()
#     paths_to_check = [
#         base_dir / "pyproject.toml",
#         base_dir / ".pre-commit-config.yaml",
#         base_dir / "tox.ini",
#         base_dir / "README.md",
#         base_dir / "LICENSE.md",
#         base_dir / "src",
#         base_dir / "tests",
#         base_dir / "src" / project_name,
#     ]
#     if fastapi:
#         paths_to_check.append(base_dir / "src" / project_name / "main.py")
#     for path in paths_to_check:
#         check_file_exists(path)
#
#
# @app.command()
# def delete_all(project_name: str, fastapi: bool = False):
#     """Deletes all files and directories associated with the project."""
#     if typer.confirm(
#         f"Are you sure you want to delete all files for '{project_name}'? This action cannot be undone."
#     ):
#         delete_project_files(project_name, fastapi)
#         typer.echo("Deletion completed.")
#     else:
#         typer.echo("Deletion cancelled.")
#
#
# @app.command()
# def setup_poetry():
#     """Check for Poetry installation and install if not present."""
#     if is_poetry_installed():
#         typer.echo("Poetry is already installed.")
#     else:
#         typer.echo("Poetry is not installed.")
#         if typer.confirm("Do you want to install Poetry now?"):
#             install_poetry()
#         else:
#             typer.echo("Poetry installation skipped.")
#
#
# @app.command()
# def create_venv():
#     """Create a virtual environment named '.venv' and configure Poetry for local virtualenv creation."""
#     try:
#         subprocess.run(
#             ["poetry", "config", "virtualenvs.create", "true", "--local"], check=True
#         )
#         typer.echo("Configured Poetry to create virtual environments locally.")
#
#         subprocess.run(["python", "-m", "venv", ".venv"], check=True)
#         typer.echo("Virtual environment '.venv' created successfully.")
#     except subprocess.CalledProcessError as e:
#         typer.echo(f"Failed to execute command: {e}")
#
#
# @app.command()
# def use_venv():
#     """Switch to using the '.venv' environment with Poetry."""
#     cwd = Path.cwd()
#
#     if not find_pyproject_toml(cwd):
#         typer.echo(
#             "Poetry could not find a pyproject.toml file in the current or parent directories."
#         )
#         raise typer.Exit()
#
#     venv_path = cwd / ".venv" / "bin" / "python"
#     if platform.system() == "Windows":
#         venv_path = cwd / ".venv" / "Scripts" / "python.exe"
#
#     if not venv_path.exists():
#         typer.echo(
#             "Virtual environment '.venv' does not exist. Please create it first."
#         )
#         raise typer.Exit()
#
#     try:
#         subprocess.run(["poetry", "env", "use", str(venv_path)], check=True)
#         typer.echo("Switched to virtual environment 'myvenv'.")
#     except subprocess.CalledProcessError as e:
#         typer.echo(f"Failed to switch to virtual environment: {e}")
#
#
# if __name__ == "__main__":
#     app()
