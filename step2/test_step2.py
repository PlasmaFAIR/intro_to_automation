import importlib.util
import pathlib
import subprocess
import sys
import venv

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
    venv.create(tmp_path / "venv", with_pip=True, symlinks=True)
    command = f"""
    source {tmp_path}/venv/bin/activate;
    python -m pip install --upgrade pip
    python -m pip install {top_level_dir}
    cd {tmp_path}
    python -c 'import miller'
    """
    status = subprocess.run(command, shell=True, capture_output=True, text=True)
    assert status.returncode == 0, status.stderr


def test_in_virtual_environment():
    assert sys.prefix != sys.base_prefix, "Not currently in a virtual environment"


def test_local_import():
    miller = importlib.util.find_spec("miller")
    assert miller is not None, "'miller' not available as module"


def test_entry_point(tmp_path):
    subprocess.run(["miller"], text=True, check=True, cwd=tmp_path)
    expected_graph = pathlib.Path(tmp_path) / "miller.png"
    assert expected_graph.is_file(), f"'miller.png' not created in {tmp_path}"
