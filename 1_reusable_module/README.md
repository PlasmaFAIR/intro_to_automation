Step 1: Reusable Module
=======================

Our script currently has hardcoded parameters which makes reusing it
difficult. We have to modify the file just to change the elongation,
for example. Although it might be set up for our current use case of
making a single graph, it's much harder to use it for something novel
-- for example, doing a parameter scan or optimising some physics. It
also creates files that we don't want to keep under version control
(`*.pyc` and `__pycache__`, `miller.png`, and so on).

Hardcoded absolute paths
------------------------

The script contains a hardcoded absolute path, which makes it very
unlikely to run anywhere except the original author's machine. You
should try to completely avoid absolute paths in your code -- they're
almost never needed. Instead, use relative paths, or -- even better --
allow the user to set paths at runtime.

> [!NOTE]
> Absolute paths are those that start with `/` on Linux/Mac, or with a
> drive letter like `C:\` on Windows. Relative paths are _relative_ to
> the current directory.

### Tasks

1. Change the absolute path to a relative path
2. Check that it now works, and commit your change

4. Run the tests for the first step with: `pytest -k step1`
   - You should only have one passing test at this point!

Housekeeping
------------

Let's do a little bit of housekeeping next. Now that you've got the
script running, we don't want to litter the project with its
outputs. While it's good to use `git` to keep track of your work, it's
also much tidier to have separate repositories for your code and
_using_ your code. `git` uses a `.gitignore` file in your project top
directory to list files and patterns

### Tasks

1. Clone https://github.com/github/gitignore somewhere else
2. Copy the contents of `Python.gitignore` and
   `Global/Linux.gitignore` into `.gitignore` in your project

   - You might also like to add the `gitignore` file corresponding to
     your text editor!
   - A quick way to create a file `C` from the contents of files `A`
     and `B` is to use `cat`:

       - `cat /path/to/file/A /path/to/file/B > /path/to/file/C`

3. Let's also add `miller.png` to the end of our `.gitignore`
4. Commit it!
5. Run the step 1 tests again -- you should get another passing test
    - If you don't, check `git status`
    - If you have a `uv.lock` file, you should add this and keep it
      under version control

**Bonus:**

- Install the `ruff` linter using `uv pip install ruff`
- Run `ruff format` -- what has it changed?
- Run `ruff check` -- what are the issues? Fix them
- Run these tools frequently!

**Advanced:**

- Set up your editor or IDE to run `ruff format` and `ruff check`
  automatically
    - Your editor/IDE might have `flake8` or `pylint` integration,
      which are similar tools to `ruff check`
    - It might also have one for `black` instead of `ruff format`


Making things reusable
----------------------

One of the simplest ways to make code reusable in other contexts is to
turn it into a function:

```python
parameter = 10
result = some_maths(parameter)
```

becomes:

```python
def do_some_maths(parameter=10):
    return some_maths(parameter)
```

"Wrapping up" code into functions lets us do things like parameter
scans, optimisation, integration -- any more importantly, testing. It
also makes it much easier for other people to build on top of our
code. Writing good, modular functions is fundamental to good software
of any kind.

If you also plot graphs in your script, it's a really good idea to put
them in separate function(s) from the rest of your code. This way, if
you only want to change the way the plots look somehow (bigger fonts,
changing the markers, location of the legend, and so on), then you
would only have to re-run the plotting function, and not the
(potentially) expensive other calculations.

We still want to be able to run our file as a script though, and we
can use a common Python idiom to do so:

```python
if __name__ == "__main__":
    print(do_some_maths())
```

If you've not seen this idiom before, just take it as some magic words
-- there is an explanation, but it's not important to understand at
this stage. The result is that the `if` statement is true _only when
we run the file as a script_, and is false if we `import` the file as
a module. In other words, when we run this script from the command
line:

```bash
$ python ./my_script.py
```

then `print(do_some_maths())` will execute. But if instead we want to
use the same file as a module in another python script or module:

```python
import my_script
```

then the `if __name__ == "__main__"` statement will be `False` and so
`print(do_some_maths())` won't execute.

With these two changes, we can now use our module both as a script as
before, _and_ `import` it to use in other code.

For various reasons that we'll come to later, it's also a good idea
to call our functions from a single function, and call _that_ as our
script code:

```python
def main():
    print(do_some_maths())

if __name__ == "__main__":
    main()
```

Note that our function `main` is nothing _really_ to do with the
`"__main__"` string here, it's just convention. Remember that
double-underscores in Python usually mean magic is happening.

Lastly, it's good practice to document your code. Python has a really
nice built in feature called docstrings:

```python
def do_some_maths(parameter=10):
    """Do some maths

    Arguments
    ---------
    parameter:
        The maths parameter
    """
    ...
```

You can see the docstring for a Python object with the builtin
function `help`:

```
Help on function do_maths in module __main__:

do_maths(parameter=10)
    Do some maths

    Arguments
    ---------
    parameter:
        The maths parameter
```

Tools like [Sphinx](https://www.sphinx-doc.org/en/master/) and
[mkdocs](https://www.mkdocs.org) can also automatically pull out
docstrings and make pretty documentation websites.

There are two main styles for Python docstrings, but personally I much
prefer [numpydoc](https://numpydoc.readthedocs.io/en/latest/format.html).

### Tasks

1. Create two functions: `flux_surface` and `plot_surface`
   - What arguments should they take?
   - What should they return?
1. To enable reuse in more contexts, add another argument `savefig` to
   `plot_surface`, defaulting to `True`, that controls whether or not
   the figure is actually saved
1. Add docstrings to the two functions
1. Call both functions from a third function `main`
1. Use the `__name__ == "__main__"` idiom to run `main`
1. Run the step 1 tests again -- now everything should pass
   - If you have issues with `matplotlib` not being able to find
     `tkinter` or `tkagg`, trying using `uv` to install `PyQt6`
1. The volume of an axisymmetric tokamak is proportional to the area
   of its cross-section. We can numerically integrate the flux surface
   to get the area:

   ```
   def area(r, z):
       # abs because (r, z) start on the out-board midplace and r decreases
       return np.abs(np.trapezoid(z, r))
   ```

   Using the Python terminal or a separate script, import `miller` and
   make a plot of area vs delta
   - What are sensible values of delta?

**Bonus:**

- Pass an optional `ax` argument to `plot_surface`. If `ax is not
  None`, plot to that axis, otherwise create a [new figure and
  axis][subplots] and plot to that. Return the actual axis you used
    - This is a useful technique for both quickly plotting with a new
      figure and also overplotting results onto existing figures
    - You may then need to switch from using the `plt` interface to
      using the object-oriented approach (`plt.plot` -> `ax.plot`)

**Advanced:**

- Add type hinting to your new functions

[subplots]: https://matplotlib.org/stable/users/explain/figure/figure_intro.html#creating-figures
