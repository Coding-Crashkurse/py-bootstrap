# py-bootstrap

## Description
`py-bootstrap` is a Python CLI application designed for easy setup and management of Python projects. It automates tasks like creating a structured project layout, setting up Poetry, managing virtual environments, and includes optional FastAPI support.

## Features
- Automated Project Initialization
- Virtual Environment Management
- Poetry Integration
- FastAPI Project Support
- File Verification

## Requirements
- Python 3.10 or higher
- Poetry for dependency management (optional)

## Installation
Install `py-bootstrap` using pip: `pip install py-bootstrap`


## Usage
Commands provided by `py-bootstrap`:

### Create a New Project
`pbs new [project_name]`

Options:
- `--default`: Use default settings.
- `--fastapi`: Initialize a FastAPI app.

### Check Project Files
`pbs check_files [project_name]`

Option:
- `--fastapi`: Check FastAPI-specific files.

### Delete All Project Files
`pbs delete_all [project_name]`

Option:
- `--fastapi`: Delete FastAPI-specific files.

### Setup Poetry
`pbs setup-poetry`


### Create a Virtual Environment
`pbs create_venv`


### Use the Virtual Environment
`pbs use_venv`


