Step 1: Reusable Module
=======================

Our script currently has hardcoded parameters which makes reusing it
difficult. We have to modify the file just to change the elongation,
for example. It also creates files that we don't want to keep under
version control (`*.pyc` and `__pycache__`, `miller.png`, and so on).

Hardcoded absolute paths
------------------------

The script contains a hardcoded absolute path, which makes it
difficult to run anywhere except the original author's machine.

1. Change the absolute path to a relative path
2. Check that it now works, and commit your change
3. Install `pytest`: `pip install pytest`
4. Run the tests for the first step with: `pytest -k step1`
   - You should only have one passing test at this point!

Housekeeping
------------

Let's do a little bit of housekeeping first.

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

**Bonus:**

- Install `black` and `ruff` using `pip`
- Run `black`
- Run `ruff` and fix the issues


Making things reusable
----------------------

One of the simplest ways to make code reusable in other contexts is to
turn it into a function:

```python
parameter = 10
result = maths(parameter)
```

becomes:

```python
def do_maths(parameter=10):
    return maths(parameter)
```

We still want to be able to run our file as a script though, and we
can use a common Python idiom to do so:

```python
if __name__ == "__main__":
    print(do_maths())
```

If you've not seen this idiom before, just take it as some magic words
-- there is an explanation, but it's not important to understand at
this stage. The result is that the `if` statement is true _only when
we run the file as a script_, and is false if we `import` the file as
a module.

With these two changes, we can now use our module both as a script as
before, _and_ `import` it to use in other code.

For various reasons that we'll come to later, it's also idea to wrap
up our functions in a single function, and call _that_ as our script
code:

```python
def main():
    print(do_maths())

if __name__ == "__main__":
    main()
```

Note that our function `main` is nothing really to do with the
`"__main__"` string here, it's just convention. Remember that
double-underscores in Python usually mean magic is happening.

Lastly, it's good practice to document your code. Python has a really
nice built in feature called docstrings:

```python
def do_maths(parameter=10):
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

There are two main styles for Python docstrings, but I much prefer
[numpydoc](https://numpydoc.readthedocs.io/en/latest/format.html).

1. Create two functions: `flux_surface` and `plot_surface`
2. `flux_surface` should take `A`, `kappa`, `delta`, and `R0` as
   inputs, with default values as the current hardcoded ones, and
   return `R_s, Z_s`
3. `plot_surface` should take `R_s` and `Z_s`
4. Add docstrings to the two functions
5. Wrap up both functions in a third function `main`
6. Use the `__main__` idiom to run `main`
7. Run the step 1 tests again -- now everything should pass

**Bonus:**

- Pass an optional `ax` argument to `plot_surface`. If `ax is not
  None`, plot to that axis, otherwise create a [new figure and
  axis][subplots] and plot to that. Return the actual axis you used


[subplots]: (https://matplotlib.org/stable/users/explain/figures.html#creating-figures)
