import pathlib
import subprocess
import textwrap


def test_command_line_args(tmp_path):
    status = subprocess.run(
        ["miller", "--help"], cwd=tmp_path, capture_output=True, text=True
    )
    assert status.returncode == 0, status.stderr
    assert "options:" in status.stdout, "Help argument unsuccessful"


def test_input_file(tmp_path):
    contents = textwrap.dedent(
        """
        [miller]
        A = 2.2
        kappa = 3.0
        delta = 0.7
        R0 = 3.2
        """
    )
    filename = tmp_path / "input.toml"
    pathlib.Path(filename).write_text(contents)

    status = subprocess.run(
        ["miller", "--filename", filename], cwd=tmp_path, capture_output=True, text=True
    )
    assert status.returncode == 0, status.stderr
    figure = tmp_path / "miller.png"
    assert figure.is_file(), f"Missing figure at '{figure}'"
