import pathlib
import sys

top_level_dir = pathlib.Path(__file__).parent.parent


def test_step0(tmp_path, monkeypatch):
    venv_dir = top_level_dir / ".venv"
    assert venv_dir.exists(), "venv not created -- run 'uv venv' to create one"

    assert sys.prefix != sys.base_prefix, "Virtual environment not activated"

    assert sys.version_info.major == 3, "Using Python 2! Make sure you're using a venv"
    assert (
        sys.version_info.minor >= 11
    ), f"Using Python 3.{sys.version_info.minor} and not >= 3.11, make sure you've used `uv` to install a newer version"

    try:
        import numpy
    except ModuleNotFoundError:
        assert False, "numpy not installed (or pytest not running in correct venv)"

    monkeypatch.syspath_prepend(top_level_dir)
    try:
        import miller
    except FileNotFoundError:
        return
