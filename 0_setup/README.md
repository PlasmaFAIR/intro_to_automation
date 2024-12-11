Step 0: Setup
=============

We're going to be mostly using standard Python tools and builtin
modules, with a couple of exceptions. This brief exercise will make
sure everything is set up correctly.

Virtual environments
--------------------

Virtual environments (or "venvs") are a really useful tool for working
on different projects. They allow you to install python packages
without affecting your whole environment. This way, you can install
incompatible versions of packages for different projects, for
instance.

There are other tools out there that can manage venvs, including the
Python builtin module `venv`. However, we're going to use `uv`
because:

a) it's *much* faster, and
b) it can also install Python for us.

To see what versions of Python are available, run:

```console
$ uv python list
cpython-3.12.8-linux-x86_64-gnu                 <download available>
cpython-3.12.7-linux-x86_64-gnu                 /usr/bin/python3.12
cpython-3.12.7-linux-x86_64-gnu                 /bin/python3.12
...
```

You should see a long list of different versions like the above (yours
might look different). Check that you have at least
`cpython-3.11.10-<suffix>` installed. If you don't you can quickly
install it with:

```console
$ uv python install 3.11
```

This is the fastest way to stay up-to-date with Python versions,
whatever system you're on.

We can create a new virtual environment with:

```console
$ uv venv
Using CPython 3.11.10
Creating virtual environment at: .venv
Activate with: source .venv/bin/activate
```

The output tells you the version of Python used (which should be the
latest available -- use `--python 3.13` for example, to use a specific
version), the directory the environment was created in (`.venv`), and
how to activate the venv (different on Windows and Linux/Mac).

The `.venv` directory basically stores a copy of the `python`
executable and all the packages you install in the virtual environment
(actually, it stores hardlinks/shortcuts to them to save space and
time), and some scripts to change your environment variables to point
to these copies. Run `deactivate` to deactivate the venv.

Venvs are lightweight and throwaway -- if you ever get your packages
in a mess for whatever reason, just delete the `.venv` directory and
make a new one.

`uv` is also a drop-in replacement for `pip`: inside a `uv` venv, we
can use `uv pip ...` instead of `pip` and get a big speed-up.

### Tasks

1. Create a virtual environment with `uv venv`
2. Activate the environment following the instructions
3. Install numpy, matplotlib, and pytest with `uv pip install numpy matplotlib pytest`
4. Run `pytest -k step0` to check you have everything set up correctly
   - If the test fails with "Virtual environment not activated", you
     might have another version of pytest installed which is being
     picked up. Try running `deactivate` and re-activating the venv
