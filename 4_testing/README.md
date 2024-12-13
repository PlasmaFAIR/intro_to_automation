Writing Tests
=============

Tests are a crucial part of developing software. Tests demonstrate
correctness of the software, as well as allowing us to make
modifications with confidence. Unfortunately, writing tests for
scientific software can be challenging -- we probably wrote the code
to solve the problem in the first place! However, there are still
tests that we can write and different ways that we can tackle this
issue.

You might notice that there are no tests in this directory -- that's
because you're going to be writing them! How will you know if the
tests themselves are correct? That is, unfortunately, a Hard Problem!

A quick refresher on basic pytest tests: pytest first looks for files
named `test*.py`, and then looks for functions called `test_*` and
runs them, gathering the output from any failed `assert`s and
displaying them all at the end. A trivial test looks like:

```
def test_always_passes():
    assert True

def test_always_fails():
    assert False
```

Most real tests looks something more like:

```
def test_simple():
    expected = [1, 2, 3]
    result = my_func()

    assert result == expected
```

Comparing results from numerical calculations to exact numbers has
some pitfalls, but luckily numpy has the handy
[`numpy.testing.assert_allclose`][allclose] which checks that two
arrays match within some tolerance, and prints useful information if
they don't:

```
import numpy.testing as npt

def test_numbers():
    expected = [1.1, 2.2, 3.3]
    result = my_func()

    npt.assert_allclose(result, expected)
```

There's a lot more than pytest can do, but this is usually enough for
most cases.

Simple Cases
------------

While we might be able to solve the full problem with pen and paper,
or at least not in a way that isn't just restating it, there are
sometimes simpler cases that we can solve. In fact, sometimes it's
even possible to push through ersatz solutions and get something we
can test, even though it might not be physically relevant.

For the Miller parameterisation, when the aspect ratio, major radius,
and elongation are all one and the triangularity is zero, the solution
is a circle.

### Tasks

1. Create a file in this directory called `test_step4.py`
2. Write a function `test_circle` that calls `flux_surface` with
   parameters for a circle
   - You might want to plot this beforehand to check you have the
     correct values!
3. Use `assert_allclose` to check that your result is a circle
4. Run your test with `pytest -k step4`


Properties
----------

Even when we can't determine the overall solution, we might still know
some properties that it must have. For example, there may be some
conserved quantity, ratio, or inequality that always holds. In other
cases, we might not know the solution everywhere, but we might know it
at some points in some limit. For these sorts of tests, it's useful to
consider both "usual" values we might expect to see, as well as more
extreme value and edge cases that might come up less frequently. These
cases can often help us find bugs in our implementations.

For our simple Miller parameterisation, flux surfaces are always
up-down symmetric about $Z=0$.

### Tasks

1. Think how you would check this property visually. You might find it
   useful to make a plot that you can inspect this property by eye.
2. Write a test that checks this for some values of $`(A, R_0, \kappa,
   \delta)`$

**Bonus:**

- Can you think of any other properties Miller flux surfaces have?
  Write tests for them. Hint: consider the min and max points of both
  $R, Z$ for extreme values of $\kappa$ and $\delta$

**Advanced:**

- Use [`pytest.mark.parametrize`][pytest_parameters] to simplify your
  test over multiple values
- Use a property testing library such as [Hypothesis][hypothesis] to
  automatically generate edge cases. For this case, you'll have to use
  their [float strategy][hypothesis_float] with explicit min and max
  values

[pytest_parameters]: https://docs.pytest.org/en/4.6.x/parametrize.html
[hypothesis]: https://hypothesis.readthedocs.io
[hypothesis_float]: https://hypothesis.readthedocs.io/en/latest/data.html#hypothesis.strategies.floats

Golden Answer
-------------

When we can't find any simple cases or nice properties that we can
test, we can always fall back on golden answers. Also called
regression tests, with these we just compare the result with that from
a previous run. Then at least any changes to the code that change the
result will be caught.

There are some downsides to this approach: it doesn't necessarily tell
you _what_ went wrong, just that something has; if we fix a bug or
make some other change that we expect to change the result, then we'll
have to update the golden answer -- and we can't be sure we've made
our original change correctly.

### Tasks

1. Write a golden answer test for some particular value of $`(A, R_0,
   \kappa, \delta)`$

[allclose]: https://numpy.org/doc/stable/reference/generated/numpy.testing.assert_allclose.html
