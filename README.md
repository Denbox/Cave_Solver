Roger Barkan's [Colossal Cave Collection](https://gmpuzzles.com/store/colossal-cave-collection) is quite hard.
In general, cave puzzles [are NP-complete](https://www2.stetson.edu/~efriedma/papers/corral/corral.html).
However, the puzzles have enough structure to make programming solvers quite nice.

This project is a backtracking cave solver in python with some nice optimizations baked in.
Thanks to [Ryan Oakley](https://github.com/RAOakley) for pairing!

Todo:
* improve heuristics
* improve forcing moves
* count backtracking steps
* handling cave problems with no solution
* handling cave problems with multiple solutions
