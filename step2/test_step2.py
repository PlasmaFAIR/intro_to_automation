import pathlib
import subprocess
import venv

top_level_dir = pathlib.Path(__file__).parent.parent


def test_install(tmp_path):
    venv.create(tmp_path / "venv", with_pip=True, symlinks=True)
    command = f"""
    source {tmp_path}/venv/bin/activate;
    python -m pip install --upgrade pip
    python -m pip install {top_level_dir}
    """
    status = subprocess.run(command, shell=True, capture_output=True, text=True)
    assert status.returncode == 0, status.stderr


def test_local_import():
    import miller
