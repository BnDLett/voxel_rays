# Voxel Rays
A project to demonstrate a theoretical way of ray tracing.

## About
While the objects are referred to as "voxels," they're more akin to pixels than they are voxels. It's also worth noting
that this is riddled with edge cases. The idea is pretty much like graphing, except you're iterating either x or y by
one. Say, for example, you were to graph a ray travelling through voxels at a slope of `1/2` — you'd use`floor(x * 1/2)`
to find the position of the y pixel. Or, in mathematical terms, `y_p = ⌊1/2x⌋`, where `y_p` is the y value of the voxel.
However, that introduces an edge case for when the slope is larger than 1, so you'll need to swap `y_p` for `x_p` and
`x` with `y` for the graph to be relatively accurate.

There is also another edge case, where numerators larger than 1 tend to not play nicely with this. You'll need a way to
detect when the ray has crossed the bottom line of another voxel. I never bothered to implement a proper solution for
this, so the program presented here isn't 100% accurate.

Given those edge cases, I'd recommend against using this — just use something such as DDA, which seems to be relatively
well known to work for voxel computations.
