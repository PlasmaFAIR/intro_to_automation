Removing hardcoded parameters
=============================

As it stands, our package can still be run as a script, but the
parameter values are still all hardcoded. In these exercises, we're
going to add the ability to set the parameters through command line
arguments and then with an input file.

Command line arguments
----------------------

The [`argparse`][argparse] module makes reading command line arguments
pretty straightforward. There are three steps to using it:

First, create an `ArgumentParser`:

```python
import argparse

parser = argparse.ArgumentParser(
    prog="ProgramName",
    description="What the program does",
    epilog="Text at the bottom of help",
)
```

Next, add arguments to the parser:

```python
parser.add_argument("filename")  # positional argument
parser.add_argument("-c", "--count")  # option that takes a value
parser.add_argument("-v", "--verbose", action="store_true")  # on/off flag
```

And then, finally, parse any command line arguments:

```python
args = parser.parse_args()
```

`args` is an [`argparse.Namespace`][namespace] object, and the
argument values can be accessed as a normal attribute:

```python
>>> args.count
"2"
```

or we can convert it to a `dict` using the builtin `vars`:

```python
>>> vars(args)
{'filename': 'some_file.txt', 'count': '2', 'verbose': True}
```

1. Create an `argparse.ArgumentParser` in your `main` function
2. Add arguments for `A`, `kappa`, `delta` and `R0`
   - Prefer using the keyword form `--argument-name` when your program
     takes multiple values, as multiple positional arguments are hard
     to read
3. Parse the arguments and pass them through to `flux_surface`

**Bonus:**

- If you set a version for your package, add a `--version` argument
  with the `store_true` action. If this is set, print the version and
  `return`

[argparse]: https://docs.python.org/3/library/argparse.html
[namespace]: https://docs.python.org/3/library/argparse.html#argparse.Namespace
