import importlib
import pathlib
import shutil
import subprocess
import sys

top_level_dir = pathlib.Path(__file__).parent.parent
script = top_level_dir / "miller.py"


def test_fixed_path(tmp_path):
    shutil.copy(script, tmp_path)
    subprocess.run(["python3", "miller.py"], check=True, cwd=tmp_path)
    expected_graph = pathlib.Path(tmp_path) / "miller.png"
    assert expected_graph.is_file(), f"'miller.png' not created in {tmp_path}"


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
