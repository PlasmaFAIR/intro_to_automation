import importlib
import pathlib
import shutil
import subprocess
import sys

import pytest

top_level_dir = pathlib.Path(__file__).parent.parent
script = top_level_dir / "miller.py"


def already_moved_script() -> bool:
    module = top_level_dir / "src" / "miller" / "__init__.py"
    return not script.exists() and module.exists()


@pytest.mark.skipif(already_moved_script(), reason="Script already moved to package")
def test_fixed_path(tmp_path):
    shutil.copy(script, tmp_path)
    subprocess.run([sys.executable, "miller.py"], check=True, cwd=tmp_path)
    expected_graph = pathlib.Path(tmp_path) / "miller.png"
    assert expected_graph.is_file(), f"'miller.png' not created in {tmp_path}"


@pytest.mark.skipif(already_moved_script(), reason="Script already moved to package")
def test_no_uncommitted_files():
    status = subprocess.run(
        ["git", "status"], check=True, capture_output=True, text=True
    )
    assert not status.stderr, "'git status' didn't run successfully"
    assert (
        "Untracked files" not in status.stdout
    ), "There are untracked files in the repo"
    existing_graph = top_level_dir / "miller.png"
    assert (
        not existing_graph.exists()
    ), "'miller.png' is in the working tree, and may be committed in the repo"


def test_has_functions():
    sys.path.append(str(top_level_dir))
    miller = importlib.import_module("miller")

    flux_surface = getattr(miller, "flux_surface", None)
    assert callable(flux_surface), "Module missing function 'flux_surface'"
    assert flux_surface.__doc__, "'flux_surface' missing docstring"

    plot_surface = getattr(miller, "plot_surface", None)
    assert callable(plot_surface), "Module missing function 'plot_surface'"
    assert plot_surface.__doc__, "'plot_surface' missing docstring"


@pytest.mark.skipif(already_moved_script(), reason="Script already moved to package")
def test_no_ruff_warnings(tmp_path):
    pytest.importorskip("ruff")

    shutil.copy(script, tmp_path)

    output = subprocess.run(["ruff", "check", tmp_path], capture_output=True)
    assert output.returncode == 0, "ruff check had some warnings"

    output = subprocess.run(["ruff", "format", "--check", tmp_path])
    assert output.returncode == 0, "ruff format modified file"
