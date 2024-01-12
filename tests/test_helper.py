import pytest
from unittest.mock import MagicMock
from subprocess import CalledProcessError
from pathlib import Path
from app.helper import (
    find_pyproject_toml,
    is_poetry_installed,
    check_file_exists,
    validate_project_name,
    validate_author_name,
)


def test_find_pyproject_toml(tmp_path):
    (tmp_path / "pyproject.toml").touch()
    # pyproject.toml exists in the current directory
    assert find_pyproject_toml(tmp_path) == True


def test_is_poetry_installed(mocker):
    mocker.patch("subprocess.run", return_value=None)
    assert is_poetry_installed() == True

    mocker.patch("subprocess.run", side_effect=CalledProcessError(1, "cmd"))
    assert is_poetry_installed() == False


def test_check_file_exists(capsys):
    mock_path = MagicMock(spec=Path)
    mock_path.__str__.return_value = "test_file"

    # Case when file exists
    mock_path.exists.return_value = True
    check_file_exists(mock_path)
    captured = capsys.readouterr()
    assert "✔ test_file" in captured.out

    # Case when file does not exist
    mock_path.exists.return_value = False
    check_file_exists(mock_path)
    captured = capsys.readouterr()
    assert "✖ test_file" in captured.out


def test_validate_project_name():
    assert validate_project_name("valid_project_name") == "valid_project_name"

    with pytest.raises(ValueError):
        validate_project_name("InvalidProjectName")


def test_validate_author_name():
    assert validate_author_name("John Doe") == "John Doe"

    with pytest.raises(ValueError):
        validate_author_name("John_Doe123")
