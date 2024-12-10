from importlib.metadata import entry_points
import importlib.util
import pathlib
import subprocess

import pytest

top_level_dir = pathlib.Path(__file__).parent.parent


def test_project_structure():
    original_file = top_level_dir / "miller.py"
    assert not original_file.exists(), "Script not moved from original directory"

    src_dir = top_level_dir / "src"
    assert src_dir.is_dir(), "Missing 'src' directory"

    package_dir = src_dir / "miller"
    assert package_dir.is_dir(), "Missing 'src/miller' directory"

    wrong_name = package_dir / "miller.py"
    correct_name = package_dir / "__init__.py"
    assert not (
        wrong_name.exists()
    ), f"Python file has wrong name ('{wrong_name}', but should be '{correct_name}')"
    assert correct_name.is_file(), f"Expected '{correct_name}', have you made a tpyo?"


def test_install(tmp_path):
    pyproject_toml = top_level_dir / "pyproject.toml"
    assert pyproject_toml.exists(), "Missing 'pyproject.toml' file at top level"

    subprocess.run(["uv", "venv"], cwd=tmp_path, check=True)
    command = f"""
    source {tmp_path}/.venv/bin/activate;
    uv pip install {top_level_dir}
    cd {tmp_path}
    python -c 'import miller'
    """
    status = subprocess.run(command, shell=True, capture_output=True, text=True)
    assert status.returncode == 0, status.stderr


def test_local_import():
    miller = importlib.util.find_spec("miller")
    assert miller is not None, "'miller' not available as module"


def test_entry_point(tmp_path):
    pytest.importorskip("miller")

    miller = entry_points(group="console_scripts", name="miller")
    assert miller, "'console_scripts' not set in 'pyproject.toml'"

    run_miller = subprocess.run(["miller"], text=True, cwd=tmp_path)
    assert run_miller.returncode == 0, f"Couldn't run `miller`: {run_miller.stderr}"

    expected_graph = pathlib.Path(tmp_path) / "miller.png"
    assert expected_graph.is_file(), f"'miller.png' not created in {tmp_path}"
