Packaging
=========

A package is a module, or collection of modules, along with some
metadata that describes things like their dependencies.

Project structure
-----------------

Packages are expected to conform to some kind of minimal project
structure, depending on exactly what tools you're using. For this,
we're going to use the very popular `setuptools`, which needs a
structure that looks something like this at a minimum:

```
.
├── pyproject.toml
└── package_name
    └── module_name.py
```

where `pyproject.toml` contains metadata about the project.

We're actually going to use one more directory to help `setuptools`
find the right files because this tutorial has some extra directories:

```
.
├── pyproject.toml
├── README.md
├── src
│   └── miller
│       └── __init__.py
├── step1
│   ├── README.md
│   └── test_step1.py
:
```

This way, when building the package, only the modules under `src` are
found, and everything else is automatically ignored. It's still
possible to use the first layout (without `src`), but it requires some
manual configuration.

<!-- TODO: README and LICENCE -->
<!-- TODO: Have students use a subdirectory for the project? -->

We also rename the file to `__init__.py` so that our functions are
immediately available when we do `import miller`.

1. Create the nested directories: `src/miller`
2. Use `git mv` to move `miller.py` under this new directory and
   change its name to `__init__.py`
   - `git mv` both moves a file and stages the change
3. Don't forget to run the tests and commit!

**Bonus:**

- Experiment with keeping the filename as `src/miller/miller.py`. Can
  you see why we've named it `src/miller/__init__.py` instead? What
  could we do if we wanted to keep it as `src/miller/miller.py`?

Metadata
--------

There is now a standard metadata format for Python packages (described
in [PEP621][PEP621]) which is specified in the `pyproject.toml`
file. [TOML](https://toml.io/en/) is a popular file format that has a
well defined syntax and semantics, and is pretty easy to read.

A `pyproject.toml` file consists of tables denoted by square brackets
`[]`, and key-value pairs separated by an equals sign `=`. The
absolute bare minimum file has one table, `[project]`, and two keys,
`name` and `version`:

```toml
[project]
name = "miller"
version = "0.1.0"
```

Note that the key names are bare and the values here are in
double-quotes `""` because they are strings.

As well as metadata about your project, one of the most important
functions of this file is to list the dependencies required to run (or
build) your code. For example, for working with data from MAST-U, you
might be using [UDA](https://ukaea.github.io/UDA/). By including this
in the list of dependencies in `pyproject.toml`, installers like `uv`
and `pip` will ensure that it is installed at the same time as your
code:

```toml
[project]
dependencies = ["uda"]
```

You can also specify which versions of dependencies your code will
work with. For example, maybe you use a function which was only added
in `scipy` 1.8 -- or maybe you're still using a class that was removed
in `numpy` 2.0:

```toml
[project]
dependencies = [
    "scipy >= 1.8",
    "numpy < 2.0.0",
]
```

Should you specify dependency versions in your `pyproject.toml`? And
if so, what versions should you use? Most of the time, all your
dependencies will work fine together, but if there are clashes between
_their_ dependencies it can be a real headache! There is a standard to
alleviate this in the scientific python ecosystem (numpy, scipy,
matplotlib, and so on) by supporting a set of minimum versions, called
[SPEC-0](https://scientific-python.org/specs/spec-0000/). Unless you
really, really need to work with older versions, following SPEC-0 is a
sensible suggestion.

The `uv.lock` file that `uv` creates is essentially a big list of the
exact versions of all your direct and indirect dependencies (the
dependencies of your dependencies). `uv` uses this file to keep things
consistent across platforms and machines. You should keep this under
version control, but otherwise you can safely ignore it.

You might also notice that SPEC-0 specifies a minimum version of
Python to support. Dropping support for older versions of python
allows libraries to use newer features and benefit from performance
improvements without waiting 5 years or more. The `requires-python`
key under `[project]` allows developers to specify what versions of
Python they support. This helps stop unexpected breakages from using
the wrong version.

One more useful feature is the ability to have optional
dependencies. This is often used if tests need extra libraries, for
instance, which wouldn't be useful to most users; or for optional
features that only a subset of users are interested in. For example,
[`xarray`][xarray] has an optional `parallel` dependency set, for parallelising
computations. Optional dependencies are specified in your
`pyproject.toml` like so:

```toml
[project.optional-dependencies]
accel = ["scipy", "bottleneck", "numbagg", "numba>=0.54", "flox", "opt_einsum"]
parallel = ["dask[complete]"]
```

and installed by naming them like this: `xarray[parallel]`; for
example with `uv`:

```console
$ uv pip install xarray[parallel]
```

(you can see another example above in xarray's `pyproject.toml`).

[PEP631][PEP631] describes the standard for specifying dependencies in
`pyproject.toml`.

### Tasks

1. Create a minimal `pyproject.toml`
2. Add the dependencies `numpy` and `matplotlib`
   - Check that the versions you use conform to SPEC-0
3. Install your project with `uv pip install .` from the top-level directory
   (where the `pyproject.toml` is)
   - `.` here is shell shorthand for "the current directory"
   - You can also give `uv pip install` a relative or absolute local path to the
     project on your computer, or a GitHub URL, as well as the more usual name
     of package on [PyPI](https://pypi.org)
4. Run the `step2` tests using `pytest`

**Bonus:**

- Add `pytest` as an optional dependency named `tests`
- Install the `tests` optional dependency

**Advanced:**

- Use [`importlib_metadata`][importlib_metadata] to set `__version__`
    - Hint: In `__init__.py`, `__name__` is the name of the package
- Use [`setuptools_scm`][setuptools_scm] to dynamically set the version
    - There are a few moving parts to this, and a couple of gotchas around
      editable installs!

> [!NOTE]
> When starting new projects, check out [`uv
> init`](https://docs.astral.sh/uv/concepts/projects/init/) to quickly
> create the basic structure, and [`uv
> add`](https://docs.astral.sh/uv/concepts/projects/dependencies/#dependency-tables)
> to manage dependencies!

Virtual environments
--------------------

We already set up a virtual environment in Step 0 to make sure we had
all of our dependencies installed. Virtual environments are also very
useful for development. You can install an "editable" version of your
package while you work on it in one virtual environment, and then
install a fixed version in another environment to use for real work.

### Tasks

1. Install your project using the `--editable` flag
   - If you completed the bonus exercises adding `pytest` as an
     optional dependency, you can install it automatically with
     `.[tests]` as the path
2. Run the tests as usual!

Entry points and scripts
------------------------

While we've now made it much easier to install our script and to use it as a
module in other tools and software, we seem to have made it more difficult to
use from the command line! To recover this ability, we can create an "entry
point", a mechanism that aids discoverability. Entry points are "ways in" to our
library or program, the functions that we expect users to call for normal
workflows.

To add a console script entry point, we need to add a key under the
`[project.scripts]` table in `pyproject.toml` with the following
syntax:

```toml
[project.scripts]
script_name = "package.module:function"
```

Note the colon `:` between `module` and `function`!

Now when we install our package, `script_name` will get installed as an
executable[^1] that runs `package.module.function()`. And now we discover the
reason for having a single function `main` that just calls both of our script
functions: `main` "wraps up" our functions into a common workflow that we can
run from the command line, while more advanced users can still those functions
directly from the library.

More advanced uses of entry points are for things like plugins to libraries --
for example, [`xarray`][xarray] defines a `backend` entry point that other
packages can use to extend the types of files `xarray` can read.

[^1]: Two things to note here:
  1. The executable will be called `script_name`, that is, you can call it by
     running `script_name`
  2. If you're not using a virtual environment, the executable will be installed
     in `~/.local/bin` by default on Linux, which might not be in your `$PATH`
     and so you'll have to edit your `~/.profile` to include:

     ```bash
     export PATH=$HOME/.local/bin:$PATH
     ```

### Tasks

1. Add an entry point called `miller` that calls your `main` function.
2. To make it available, you'll need to reinstall your package
   - Don't forget to install with `--editable` so that future changes
     to the code will get picked up
3. Check it works by running `miller` from the command line
   - Try changing directory and running it somewhere else
4. Run the step 2 tests

Now we're back to where we started, with a script we can call from the
command line! Except now we have something that we can use in other
tools, and is also easier to get installed along with all of its
dependencies -- useful not just for other people, but for us too if we
start using other machines.


[PEP621]: https://peps.python.org/pep-0621
[PEP631]: https://peps.python.org/pep-0631
[setuptools_scm]: https://github.com/pypa/setuptools_scm/#pyprojecttoml-usage
[xarray]: https://xarray.dev
