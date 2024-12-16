Outputs
=======

Currently we don't save our results. For this toy problem, this is obviously not
an issue, as it takes a fraction of a second to run. For real problems though,
we usually do want to save our results! There are many, many different ways we
could choose to do this, but they fall into two broad categories: text and
binary.

Text files are almost always human-readable with basic tools like `less`,
usually pretty easy to create (at least for simple structured data), and easy to
pass around.

The downsides tend to be they are not very space-efficient when dealing with
larger volumes of data, can lose precision, get complicated when the data
becomes more structured or higher dimensional, can be fragile or difficult to
read, and may not capture important metadata.

Binary files, on the other hand, require special tools or libraries to read,
which makes them potentially more difficult to share (as you'll also need to
make sure the recipient has a compatible version), but tend to be much more
space-efficient, store the exact numbers, and allow the reader to automatically
parse and discover more structured data.

Whatever format we choose, it's also a good idea to store some provenance
information: extra metadata that enables the reader to know how the data was
generated. For example, we could store:

- all our input values
- the name and version of the software
- the date and time the file was created

For compiled software, we might also want to store extra metadata, like how the
software was built. Ideally, we want to capture as much information as possible
that would allow someone to recreate our output. This might include versions of
libraries we're using -- this is the purpose of keeping the `uv.lock` file under
version control.

Lastly, it's also a good idea to store extra metadata to give the reader more
information. The climate forecasting community have a set of conventions for
this extra metadata, the [CF-conventions][cfconventions], which the plasma
community has partly (and informally) adopted -- notably, the `long_name` and
`units`, which add a description and units to variables. For example, we might
store a variable `B0`, with a `long_name` of "magnetic field on axis" and
`units` of `T`. Storing this information requires more machine-readable
structure in our output files, for example using JSON files instead of CSV, or
something like netCDF.

[cfconventions]: https://cfconventions.org/cf-conventions/cf-conventions.html

netCDF
------

[netCDF][netcdf] is a self-describing, hierarchical file format designed for
scientific data. What this means is that the data is stored in something
resembling a directory structure, with variable names and metadata, and labelled
coordinates.

Here's an example of a netCDF file structure:

```
/
├── r
│   ├── long_name: minor radius
│   └── units: m
├── theta
├── time
│   └── units: s
├── B(r, theta)
│   ├── long_name: magnetic field
│   └── units: T
├── q(theta)
│   └── long_name: safety factor
├── p(time, r, theta)
│   ├── long_name: pressure
│   └── units: Pa
├── n(time, r, theta)
│   ├── scale: 1e19
│   ├── long_name: density
│   └── units: m^-3
├── walls/
│   ├── R(r, theta)
│   └── Z(r, theta)
└── fluxes/
    └── heat(time)
        ├── long_name: heat flux
        └── units: Q_qB
```

Variables are either dimensions (`r`, `theta`, `time`), or defined on those
dimensions (`B(r, theta)`). Variable names are the conventional physics terms
used in equations (`n`, `B`), with `long_name` and `unit` attributes that help
clear up ambiguities (is `r` the minor radius, or the major radius? Is it
defined in normalised units or SI?).

To write a file like the above using the [`netCDF4`][netcdf-python] library
looks something like this:

```python
import netCDF4

with netCDF4.Dataset("filename.nc", "w") as f:
    r_dim = f.createDimension("r", len(r))
    theta_dim = f.createDimension("theta", len(theta))

    B_var = f.createVariable("B", "f8", ("r", "theta"))
    B_var[:] = B_values
    B_var.long_name = "magnetic field"
    B_var.units = "T"

    q_var = f.createVariable("q", "f8", "r")
    q_var[:] = q_values
    q_var.long_name = "safety factor"
```

This is quite verbose and error-prone, so instead we're going to use we're going
to use [`xarray`][xarray] which abstracts over some of the details, and allows
us to take advantage of the labelled coordinates in our code as well.

```python
import xarray as xr

ds = xr.Dataset(
    {
        "B": (("r", "theta"), B, {"long_name": "magnetic field", "units": "T"}),
        "q": ("r", q, {"long_name": "safety factor""}),
    },
)

ds.to_netcdf("filename.nc")
```

This is a lot shorter! Basically we pass a `dict` of `name` keys with values as
tuples of dimension names, values, and a `dict` of attributes. We can then write
the dataset to netCDF, or one of several other file types.

So far we have made named _dimensions_ but not given them values. So in our file
`theta` only has the values `0...N-1`. NetCDF (and xarray) allow us to create
_coordinates_, which are dimensions with values, that is, the values $[0, 2\pi]$
for `theta`. In plain netCDF this is done by making a variable with the same
name as the dimension, and in xarray, these are specified through a separate
`coords` argument to `xr.Dataset`.

Xarray is a lot more powerful than this, and is particularly useful for
plotting, as it automatically takes care of labelling the axes, including with
units (assuming the variables have the `units` attribute!).

### Tasks

1. Consider the two files, [file 1](./example.geqdsk) and [file 2](./example.json).
   File 1, first 25 lines:

   ```
    FreeGS 23/03/2023  0  0ms 3  69 175
    0.337981729E+01 0.891201051E+01 0.247023022E+01 0.774079181E+00 0.000000000E+00
    0.319069873E+01 0.000000000E+00 0.000000000E+00 0.216552103E+01 0.236591466E+01
    0.206432536E+08 0.000000000E+00 0.000000000E+00 0.319069873E+01 0.000000000E+00
    0.000000000E+00 0.000000000E+00 0.216552103E+01 0.000000000E+00 0.000000000E+00
    0.510573564E+01 0.522667789E+01 0.518537716E+01 0.543472929E+01 0.530981584E+01
    0.524213790E+01 0.527901329E+01 0.560723186E+01 0.540389160E+01 0.536367108E+01
    0.544136714E+01 0.561275696E+01 0.567695733E+01 0.576859522E+01 0.597557279E+01
    0.593802953E+01 0.585829592E+01 0.613329458E+01 0.579818340E+01 0.594698431E+01
    0.589955540E+01 0.617387844E+01 0.591288854E+01 0.581511348E+01 0.624473493E+01
    0.626808376E+01 0.583385462E+01 0.589100299E+01 0.607722383E+01 0.585478504E+01
    0.634291551E+01 0.618313334E+01 0.627478489E+01 0.605180223E+01 0.608983058E+01
    0.624711320E+01 0.639415595E+01 0.634133325E+01 0.581125871E+01 0.583209907E+01
    0.618716446E+01 0.583390608E+01 0.624042595E+01 0.610989428E+01 0.624750112E+01
    0.596378214E+01 0.597467134E+01 0.594744925E+01 0.598993089E+01 0.639928712E+01
    0.599035661E+01 0.614024792E+01 0.603865118E+01 0.590141894E+01 0.597465167E+01
    0.605314141E+01 0.600917843E+01 0.628661846E+01 0.605996164E+01 0.601046096E+01
    0.627305607E+01 0.592002845E+01 0.583439773E+01 0.604093703E+01 0.599283119E+01
    0.626803843E+01 0.629216510E+01 0.602580315E+01 0.593202186E+01
    0.143407873E+07 0.146251975E+07 0.144101071E+07 0.141804747E+07 0.132704621E+07
    0.126236183E+07 0.130555758E+07 0.124546737E+07 0.125066374E+07 0.125357044E+07
    0.114975069E+07 0.114147134E+07 0.113494148E+07 0.108698114E+07 0.104934914E+07
    0.102854369E+07 0.101914136E+07 0.100814514E+07 0.921014633E+06 0.957911824E+06
    0.928076641E+06 0.908080419E+06 0.864994409E+06 0.815578549E+06 0.777742612E+06
    0.752699147E+06 0.758974730E+06 0.690972946E+06 0.694907237E+06 0.655816365E+06
    ...
   ```

   File 2, first 25 lines:

   ```json
   {
     "comment": "FreeGS 23/03/2023  0  0ms",
     "shot": 3,
     "nx": 69,
     "ny": 175,
     "rdim": 3.37981729,
     "zdim": 8.91201051,
     "rcentr": 2.47023022,
     "rleft": 0.774079181,
     "zmid": 0.0,
     "rmagx": 3.19069873,
     "zmagx": 0.0,
     "simagx": 0.0,
     "sibdry": 2.16552103,
     "bcentr": 2.36591466,
     "cpasma": 20643253.6,
     "fpol": [
       5.10573564,
       5.22667789,
       5.18537716,
       5.43472929,
       5.30981584,
       5.2421379,
       5.27901329,
       5.60723186,
   ...
   ```

   Which would you prefer to receive from a collaborator? The first format is
   the (unfortunately ubiquitous) "geqdsk" format used by EFIT to store tokamak
   equilibrium data, while the second is the same data converted to JSON. How
   easily can you find tools to read these two files? How could we further
   improve the JSON output? What information would we need to convert this to
   netCDF?
2. Write a new function that creates an `xarray.Dataset` for your code that
   stores all your inputs, outputs, and sufficient other metadata.
3. Add a new command-line argument `--output` to save this data to netcdf. Allow
   the user to specify the filename.
4. Your package now depends on `xarray` -- make sure to modify your
   `pyproject.toml`
5. Add a coordinate for `theta`. This is currently only used internally, so
   you'll need to return it and modify other places as appropriate.

**Bonus:**

- Work through the ["xarray in 45 minutes" tutorial][xarray-tutorial].

[netcdf]: https://www.unidata.ucar.edu/software/netcdf/
[netcdf-python]: https://unidata.github.io/netcdf4-python
[netcdf-vars]: https://unidata.github.io/netcdf4-python/#variables-in-a-netcdf-file
[xarray]: https://docs.xarray.dev/en/stable/
[xarray-tutorial]: https://tutorial.xarray.dev/overview/xarray-in-45-min.html
