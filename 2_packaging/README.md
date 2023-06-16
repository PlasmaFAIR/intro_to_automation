Packaging
=========

A package is a module, or collection of modules, along with some
metadata that describes things like their dependencies.

**Note:** one of the tests for this step, `test_install` can take
~10-15 seconds to run, so don't worry if it takes awhile! You can use
`pytest -k "step2 and not install"` to run the step 2 tests and skip
just that one.

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
found, and everything else is automatically ignored.

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
in [PEP518][PEP518]) which is specified in the `pyproject.toml`
file. [TOML](https://toml.io/en/) is a popular file format that has a
well defined syntax and semantics, and is pretty easy to read.

A `pyproject.toml` file consists of tables denoted by square brackets
`[]`, and key-value pairs separated by an equals sign `=`. The minimum
file has one table, `[project]`, and two keys, `name` and `version`:

```toml
[project]
name = "miller"
version = "0.1.0"
```

Note that the key names are bare and the values here are in
double-quotes `""` because they are strings.

This is enough to be able to install your package with `python3 -m pip
install .`, but there are a couple more useful keys and
tables. `dependencies` is a list of other packages required to run
your package, `[project.optional-dependencies]` is a table specifying
other packages that are useful but not required, for example for tests
or documentation. [PEP631][PEP631] describes the standard for
specifying dependencies in `pyproject.toml`.

1. Create a minimal `pyproject.toml`
2. Add the dependencies `numpy` and `matplotlib`
3. Run the `step2` tests using `pytest`

**Bonus:**

- Add `pytest` as an optional dependency named `tests`
- Use [`setuptools_scm`][setuptools_scm] to dynamically set the version

Virtual environments
--------------------

Virtual environments are a really useful tool for working on different
projects. They allow you to install python packages without affecting
your whole environment. This way, you can install incompatible
versions of packages for different projects, for instance.

Virtual environments are also very useful for development. You can
install an "editable" version of your package while you work on it in
one virtual environment, and then install a fixed version in another
environment to use for real work.

1. Create a virtual environment with `python3 -m venv <name>` (I
   usually use the imaginative name "venv")
2. Activate the environment with `source <name>/bin/activate`
3. Install your project using the `--editable` flag
   - `pip` can install from local paths (as well as package names from
     PyPI, the usual, and URLs of Github projects too), you can use
     the Unix shortcut `.` to refer to the current directory
   - You'll probably also need to install `pytest` from inside the
     virtual environment as well to pass some of the tests
   - If you completed the bonus exercises adding `pytest` as an
     optional dependency, you can install it automatically with
     `.[tests]` as the path
4. Run the tests

Entry points and scripts
------------------------

While we've now made it much easier to install our script and to use
it as a module in other tools and software, we seem to have made it
more difficult to use from the command line. To recover this ability,
we can create an "entry point", a mechanism that aids discoverability.

To add a console script entry point, we need to add a key under the
`[project.scripts]` table in `pyproject.toml` with the following
syntax:

```toml
[project.scripts]
script_name = "package.module:function"
```

Now when we install our package, `script_name` will get installed as
an executable that runs `package.module.function()`. And now we
discover the reason for wrapping up our script functions in one more
function `main`.

1. Add an entry point called `miller` that calls your `main` function.
2. To make it available, you'll need to reinstall your package
   - Don't forget to install with `--editable` so that future changes
     to the code will get picked up

Now we're back to where we started, with a script we can call from the
command line! Except now we have something that we can use in other
tools, and is also to get installed -- useful not just for other
people, but for us too if we start using other machines.


[PEP518]: https://peps.python.org/pep-0518
[PEP631]: https://peps.python.org/pep-0631
[setuptools_scm]: https://github.com/pypa/setuptools_scm/
