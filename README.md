Roger Barkan's [Colossal Cave Collection](https://gmpuzzles.com/store/colossal-cave-collection) is quite hard.
However, cave puzzles in general are amenable to a programmatic solution, with interesting optimizations to be made.

This is currently a mostly working solution that ignores the rule about making sure that the "cave" is a single connected component. Additionally, I currently assume there exists a unique solution to the cave puzzle.

The code uses a backtracking algorithm in python to eventually exhaust all possibilities. It's set up so that making it faster via a few helper functions shouldn't be too difficult.

Currently the best candidates for speedups are:
* `forcing_moves` - a function that makes moves that don't require guessing. In a well designed cave puzzle (with a comparatively well designed forcing_moves function), this should solve it without backtracking!
* `heuristic_ordering` - a function that picks where to place the next square. Right now this traverses like a nested for loop over `x` and `y` indices, but a better choice would be to place up/down/left/right around each hint to minimize backtracking.

There is also some work required that isn't about optimization.
* `disconnected_cave` - allows us to account for the final criteria we missed to solve cave puzzles. It should involve some fun graph algorithm work!
* handling cave problems with no solution
* handling cave problems with multiple solutions
