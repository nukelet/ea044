# Branch and bound

This is an implementation of the branch and bound algorithm, for the class EA044 - Planning and Analysis of Production Systems.

It solves integer linear programming problems in the following form:

$$ \text{minimize } \mathbf{c}^T \mathbf{x} $$

$$ \text{subject to: } \mathbf{Ax} \leq \mathbf{b} $$

$$ \mathbf{x} \geq 0, \text{  } \mathbf{x} \in \mathbf{Z}^n $$

It uses an input file in the following form:

```
n p                         # n = number of variables; p = number of constraints
                            # necessary blank line!
c_1 c_2 ... c_n             # coefficients of vector "c"
                            # necessary blank line!
A_11 A_12 ... A_1n          # coefficients of matrix A
...
A_p1 A_p2 ... A_pn
                            # necessary blank line!
b_1 b_2 ... bn              # coefficients of vector "b"
```

So, for example, the following 3 variables/3 constraints problem (`tests/test_3.txt`)

$$ \text{minimize } -3 x_1 + -21 x_2 + -26 x_3 $$

$$ \text{subject to:} $$

$$ x_1 - x_2 + x_3 \leq 9 $$

$$ 6 x_2 + 5 x_3 \leq 10 $$

$$ 3 x_1 - 4 x_3 \leq 3 $$

is represented by the following data:

$$ n=3 $$

$$ p=3 $$

$$ \mathbf{c} = (-3, -21, -26) $$

$$ \mathbf{A} = \begin{bmatrix} 1 & -1 & 1 \\\ 0 & 6 & 5 \\\ 3 & 0 & -4 \end{bmatrix} $$

$$ \mathbf{b} = (9, 10, 3) $$

which is then translated to the following input file (**note**: the blank lines are necessary!):

```
3 3

-3 -21 -26

1 -1 1
0 6 5
3 0 -4

9 10 3

```

# Instructions

## Requirements

In order to run this, you **must** have the following Python libraries installed:

- `scipy >= 1.11`
- `numpy >= 1.26`

## Running

From within the `branch-and-bound` folder in this directory, you should run it as follows:

```sh
$ python bnb.py [file]
```

where `file` is the path to the file with the program data as described above.
The program will show a step-by-step description of the branch-and-bound decision tree it is traversing in order to solve the problem.

Additionally, running the program with the `--check-solution` flag:

```sh
$ python bnb.py [file] --check-solution
```

will additionally check the program's solution against the solution of the [HiGHS MILP solver](https://highs.dev/), verifying if 
the answers are equal.

## Running on the browser with `replit`

This program can be run on your browser within a `replit` container ([link](https://replit.com/@nukelets/ea044)), where it will
run the tests in `tests/test_{1,2,3}.txt`.
