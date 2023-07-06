<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">
<img alt="Creative Commons Licence" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" />
</a>
<br />This work is licensed under a <a rel="license"
href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons
Attribution-ShareAlike 4.0 International License</a>.

Automate Your PhD
=================

This project will take you through turning a script with hardcoded
parameters into a reusable package that is easier to use, more
flexible, and can be used to automate your research.

Requirements
------------

You'll need Python 3.8+ and `pip` installed, and a moderate amount of
Python knowledge. While this tutorial uses Python, many of the
techniques we'll go through are more broadly applicable to most other
programming languages.

Overview
--------

Start by forking this project on GitHub, and cloning it locally. Then
work through the four steps:

1. Reusable module
2. Packaging
3. Input
4. Testing

Each step comes with a set of tests that you should run after each
exercise. The tests will start off all failing, and successfully
completing each exercise will make more and more tests pass. You can
use this to assess your progress through the whole tutorial.

There are some **bonus** and **advanced** exercises throughout this
tutorial. Bonus exercises are good to go through if you find you have
some extra time during the session, and are about techniques that are
generally useful to most people. Advanced exercises, on the other
hand, are usually a bit more specialist, or require a bit more time
and/or research to implement. They are good next steps for the
interested learner to look into after the session.

Background: Miller Geometry
===========================

A local equilibrium of the magnetic field of a tokamak can be
represented with the so-called Miller parameterisation, defined in
[Phys. Plasmas, Vol. 5, No. 4, April 1998 Miller et al.][1]:


```math
\begin{align}
R_s(r, \theta) &= R_0 + r \cos[\theta + (\sin^{-1}\delta) \sin(\theta)] \\
Z_s(r, \theta) &= r \kappa \sin(\theta)
\end{align}
```

where $`R_s, Z_s`$ are the major radius and vertical coordinate of the
flux surface, $`R_0`$ is the major radius of the magnetic axis, $`A`$
is the aspect ratio, $`r = R_0 / A`$ is the minor radius of the flux
surface, $`\theta`$ is the geometric poloidal angle, $`\kappa`$ is the
elongation, and $`delta`$ is the triangularity.

The three parameters, $`A, \kappa, \delta`$ give a nice, simple
representation of a single flux surface. To be useful in practice, for
example in order to calculate the poloidal magnetic field, we actually
need a few more parameters, but as this is just a toy to demonstrate
software development practices, we won't concern ourselves with them
here.

![An example of a Miller parameterised flux surface](.images/example_plot.png "An example of a Miller parameterised flux surface")

[1]: https://doi.org/10.1063/1.872666
