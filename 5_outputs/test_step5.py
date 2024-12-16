import importlib
import pathlib
import subprocess
import tomllib


top_level_dir = pathlib.Path(__file__).parent.parent


def test_set_xarray_in_pyproject():
    pyproject_toml = top_level_dir / "pyproject.toml"

    with pyproject_toml.open("rb") as f:
        contents = tomllib.load(f)

    dependencies = contents["project"]["dependencies"]
    has_xarray = any(["xarray" in dep for dep in dependencies])
    assert has_xarray, "Missing 'xarray' from 'project.dependencies'"


def test_save_output(tmp_path):
    filename = "test.nc"
    run_miller = subprocess.run(
        ["miller", "--output", filename], text=True, cwd=tmp_path
    )
    assert (
        run_miller.returncode == 0
    ), f"Couldn't run `miller --output test.nc`: {run_miller.stderr}"

    output_file = tmp_path / filename
    assert output_file.exists(), f"Output file was not created at {output_file}"

    has_xarray = importlib.util.find_spec("xarray")
    assert has_xarray, "xarray not installed in current environment"

    import xarray as xr

    ds = xr.open_dataset(output_file)

    assert "R" in ds, "Missing 'R' from dataset"
    assert "theta" in ds.coords, "Missing 'theta' coordinate"
