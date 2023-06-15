Automate Your PhD
=================

0. Remove hardcoded paths
1. Convert to functions
2. Turn it into a package
3. Remove hardcoded parameters
4. Add tests

Miller Geometry
===============

Local equilibrium representation defined as in: [Phys. Plasmas,
Vol. 5, No. 4, April 1998 Miller et al.][1]


```math
R_s(r, \theta) = R_0 + r * \cos[\theta + (\sin^{-1}\delta) * \sin(\theta)]
Z_s(r, \theta) = r * \kappa * \sin(\theta)

r = R_0 / A
```

where $`R_s, Z_s`$ are the major radius and vertical coordinate of the
flux surface, $`R_0`$ is the major radius of the magnetic axis, $`r`$
is the minor radius of the flux surface, $`A`$ is the aspect ratio,
$`\kappa`$ is the elongation, and $`delta`$ is the triangularity.

[1]: https://doi.org/10.1063/1.872666
