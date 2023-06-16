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

This can be particularly useful if the command line arguments have the
same names as your function arguments, as we can use the
dict-unpacking "double splat" operator:

```python
do_some_maths(**vargs(args))
```

although you may have to remove or add other arguments. As with
everything in writing software, it depends!


1. Create an `argparse.ArgumentParser` in your `main` function
2. Add arguments for `A`, `kappa`, `delta` and `R0`
   - Prefer using the keyword form `--argument-name` when your program
     takes multiple values, as multiple positional arguments are hard
     to read
   - The [`type`][argparse_type] argument to `add_argument` can be
     used to ensure the value is converted to the correct type
3. Parse the arguments and pass them through to `flux_surface`

**Bonus:**

- If you set a version for your package, add a `--version` argument
  with the `store_true` action. If this is set, print the version and
  `return`

Input files
-----------

Command line arguments are really great for quickly trying out
options, but it can be tricky to record what options were used for a
particular run. Instead, it's often much better to use input
files. These can be kept alongside the corresponding outputs, and
shared with others to enable them to reproduce and build on top of
your work.

There are many different file formats that you might consider when
choosing one for your input files. Some that you might consider:

- JSON: very popular, implementations in most programming languages,
  but lacks comments and can be difficult for humans to write
- YAML: also very popular with many implementations, but has several
  gotchas and is notoriously complex
- INI: simple and flexible, with a loose syntax, with many different
  dialects or flavours
- TOML: essentially INI with a formal syntax

We've briefly encountered TOML with our `pyproject.toml`, and from
Python 3.11 it's in the standard library.

For earlier versions of Python, we can use the [`tomli`][tomli]
library. This is very fast, although the downside is that it can't
write files. For this exercise, that won't matter.

Using `tomli` is pretty simple: `tomli.load()` works with file handles
(as returned from `open` -- but note we need to open in `"rb"` mode)
and `tomli.loads()` works with strings directly. Both of them return a
Python dict. The simplest way to read a file is like this:

```python
with open(filename, "rb") as f:
    data = tomli.load(f)
```

1. Add `tomli` to your project dependencies, and then `pip install`
   your project to automatically download it
   - Don't forget to use `--editable` or `-e` while developing!
2. Add a new argument `--filename` to your `parser`. You'll want to
   pass `default=None` to `add_argument` so that it has some default
   value. The [`argparse`][argparse_default] has some more information
   on this argument.
3. After parsing the command line arguments, if a filename has been
   passed, use `tomli.load` to read the input file
4. Extract the Miller parameters from the data, use them instead of
   the other command line arguments
   
Here's an example input file that your program should be able to
handle:

```toml
# An example input file
[miller]
A = 2.2     # Aspect ratio
kappa = 3.0
delta = 0.7
R0 = 3.2
```


**Bonus:**

- Try to avoid calling `flux_surface` in two different places. Code is
  often easier to maintain if you don't repeat yourself.
- Can you allow command line arguments to override values set in the
  input file?


[argparse]: https://docs.python.org/3/library/argparse.html
[argparse_default]: https://docs.python.org/3/library/argparse.html#default
[argparse_type]: https://docs.python.org/3/library/argparse.html#type
[namespace]: https://docs.python.org/3/library/argparse.html#argparse.Namespace
[tomli]: https://github.com/hukkin/tomli
