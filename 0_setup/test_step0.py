import pathlib

top_level_dir = pathlib.Path(__file__).parent.parent


def test_step0(tmp_path, monkeypatch):
    venv_dir = top_level_dir / ".venv"
    assert venv_dir.exists(), "venv not created -- run 'uv venv' to create one"

    try:
        import numpy
    except ModuleNotFoundError:
        assert False, "numpy not installed (or pytest not running in correct venv)"

    monkeypatch.syspath_prepend(top_level_dir)
    try:
        import miller
    except FileNotFoundError:
        return
