import importlib.util
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

    has_numpy = importlib.util.find_spec("numpy")
    assert has_numpy, "numpy not installed (or pytest not running in correct venv)"
    has_matplotlib = importlib.util.find_spec("matplotlib")
    assert (
        has_matplotlib
    ), "matplotlib not installed (or pytest not running in correct venv)"

    monkeypatch.syspath_prepend(top_level_dir)
    try:
        # We want to actually import the file and observe its side-effects
        import miller  # noqa: F401
    except FileNotFoundError:
        return
