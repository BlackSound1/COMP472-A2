# COMP472-A2

## Link to repository: https://github.com/BlackSound1/Solving-S-Puzzles-With-Search-Algorithms

## How to run:
- If you want to input your own puzzles and goal state:
  
    1. Ordinarily, the program generates 20 random puzzles and performs all actions on those. If you want to 
run a specific puzzle or set of puzzles, please create a file called `input_puzzles.txt` and put it in the `input` 
directory. In this file, each puzzle must be on a new line and be written in a comma-separated tuple of tuples.
Each sub-tuple in the tuple of tuples must be of the same size, and there must be a number of sub-tuples equal to the size of 
each sub-tuple.

        For instance, `((1,2),(3,4))` is a valid puzzle, but something like `[[1], [2,3]]` is not.

    2. Additionally, you must create a file called `goal_state.txt` containing the one possible goal-state, and put it 
       in the `input` directory. This file must have only 1 line. The rules for how a goal-state are to be written are 
       the same as above. There are no rules as to the order of elements in the goal-state, but when *automatically* 
       generating puzzles and goal-states, a strictly ascending goal-state is generated.

    3. Finally, in the `main.py` file, comment-out the `create_20_random_puzzles()` function call to avoid automatic puzzle 
and goal-state generation.

    4. Then run as normal. `py src/main.py`
    
- If you want to run the code normally, i.e. using automatic puzzle and goal-state generation:

    1. Run the code as normal
    
Either way, be prepared for a long execution time, as DFS with or without iterative deepening is very slow for 
all puzzle sizes greater than 3x3.

The results of each puzzle (including search path and solution path) are organized by algorithm (and in the case
of A* by heuristic as well) in the `output` directory. The contents of the `output` directory are ignored using 
`.gitignore` and are not shown on GitHub. This is because they are many documents that are always changing upon every 
execution of the code. There is no reason for version control in the case of these files. 

Special Note: This software makes use of the `os.makedirs()` method. According to official Python 3 documentation 
(found here: https://docs.python.org/3/library/os.html), 
> `makedirs()` will become confused if the path elements to create include `pardir` (eg. “..” on UNIX systems).

This software does indeed use the `..` character sequence to shorten path names. If this is a problem on your system,
it is advisable to replace these relative path names with absolute path names.
Of special importance is the `directory` variable in the `output_to_files()` function definition in `functions.py`,
as it is this `directory` variable which directly interacts with `os.makedirs()`.
