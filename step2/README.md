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
│       └── miller.py
├── step1
│   ├── README.md
│   └── test_step1.py
:
```

This way, when building the package, only the modules under `src` are
found, and everything else is automatically ignored.

1. Create the nested directories: `src/miller`
2. Use `git mv` to move `miller.py` under this new directory
   - `git mv` both moves a file and stages the change
3. Don't forget to commit!

Metadata
--------

There is now a standard metadata format for Python packages (described
in [PEP518](https://peps.python.org/pep-0518/)) which is specified in
the `pyproject.toml` file. [TOML](https://toml.io/en/) is a popular
file format that has a well defined syntax and semantics, and is
pretty easy to read.

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
or documentation.

1. Create a minimal `pyproject.toml`
2. Add the dependencies `numpy` and `matplotlib`
3. Run the `step2` tests using `pytest`

**Bonus:**

- Add `pytest` as an optional dependency
- Use `setuptools_scm` to dynamically set the version

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
4. Run the tests

Entry points and scripts
------------------------

`[project.scripts]`

`main` function
