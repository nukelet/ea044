from math import floor, ceil, inf
from os import error
from typing import Optional
from scipy.optimize import linprog
from argparse import ArgumentParser, BooleanOptionalAction

'''
Test if a float value is close enough to an integer, and returns
the nearest integer value if so.
'''
def is_integer(n: float, epsilon: float = 1e-5) -> bool:
    return abs(n - round(n)) < epsilon
    
'''
Test if all entries in a solution are integers.
'''
def is_integer_solution(solution: list[float]) -> bool:
    for x in solution:
        if not is_integer(x):
            return False
    return True


'''
Get the index of the variable with the largest (closest to .5) fractional part.
'''
def get_largest_frac_part_index(current_solution: list[float]) -> int:
    chosen_i = 0
    min_diff = inf
    for (i, x) in enumerate(current_solution):
        current_diff = abs((x % 1) - 0.5)
        if current_diff <= min_diff:
            chosen_i = i
            min_diff = current_diff
    return chosen_i


'''
Get the next branches based on the solution for the current branch.

Each B&B branch is represented by a list of variable bounds,
e.g. 3 <= x1 <= 4, 4 <= x2 <= inf, and so on. This function looks
for the variable with the largest fractional part (i.e., fractional
part closest to .5) and outputs new left and right child branches:
x_i <= floor(x_i) and x_i >= ceil(x_i)
'''
def get_next_branches(current_solution: list[float],
                      current_bounds: list[tuple[float, float]]) \
                      -> tuple[list[tuple[float, float]], list[tuple[float, float]]]:
    i = get_largest_frac_part_index(current_solution)
    x = current_solution[i]
    print(f"chosen x_{i} = {x}, branching into x_{i} <= {floor(x)} and x_{i} >= {ceil(x)}")
    lower, upper = current_bounds[i]
    if upper is None:
        upper = inf

    # investigate x[i] <= floor(x[i])
    lbounds = list(current_bounds)
    lbounds[i] = (lower, min(floor(x), upper))

    # investigate x[i] >= ceil(x[i])
    rbounds = list(current_bounds)
    rbounds[i] = (max(lower, ceil(x)), upper)
    
    return lbounds, rbounds


def print_branch(bounds: list[tuple[float, float]]) -> None:
        for (i, bound) in enumerate(bounds):
            if bound == (0, None):
                continue
            left = bound[0]
            right = "inf" if bound[1] is None else bound[1] 
            print(f"({left} <= x_{i} <= {right}) ", end='')
        print("")


def print_branch_stack(stack: list[list[tuple[float, float]]]) -> None:
    print("branch stack:")
    for branch in stack:
        print("> ", end='')
        print_branch(branch)


'''
Calculate the solution to an integer linear programming problem using branch-and-bound.

This solves problems in the following form
(as defined in https://en.wikipedia.org/wiki/Integer_programming):

minimize c*x
subject to A*x <= b
x >= 0 and integers

This implementation of branch-and-bound searches the solution space with a depth-first search.
'''
def bnb(c: list[float], A: list[list[float]], b: list[float]) \
        -> tuple[Optional[float], Optional[list[int]]]:
    total_iterations: int = 0
    stack = []
    best_value: float = inf
    best_solution: Optional[list[float]] = None

    initial_bounds = [(0, None)] * len(c)
    stack.append(initial_bounds)

    while len(stack) > 0:
        total_iterations += 1
        print("--------------------------")
        print(f"[iteration {total_iterations}]")
        print_branch_stack(stack)
        current_bounds = stack.pop() 

        print("investigating: ", end='')
        print_branch(current_bounds)

        result = linprog(c, A, b, bounds=current_bounds)
        if not result.success:
            print(f"discarding: unfeasible solution!")
            continue

        current_value = result.fun
        current_solution = result.x

        print(f"current solution: {current_solution}, val={current_value}")
        print(f"best known integer solution: {best_solution}, val={best_value}")

        if current_value > best_value:
            print(f"not branching: current value ({current_value}) is worse than best known value ({best_value})")
            continue

        if is_integer_solution(current_solution):
            if current_value < best_value:
                print(f"new best integer solution found: {current_solution}, val={current_value}")
                best_value = current_value
                best_solution = current_solution
                continue
            else:
                print(f"rejecting integer solution (worse than best)")

        stack += get_next_branches(current_solution, current_bounds)

    print(f"\n******* FINISHED AFTER {total_iterations} ITERATIONS *******\n")
    print("--------------------------\n")

    if best_solution is None:
        return (None, None)

    integer_solution = list(map(lambda x: round(x), best_solution))
    return best_value, integer_solution


def parse_problem(contents: str) -> tuple[list[float], list[list[float]], list[float]]:
    lines = contents.splitlines()

    # parse problem dimensions
    var_count, constr_count = tuple(int(n) for n in lines.pop(0).split(" ")[0:2])
    print(f"variables: {var_count}, constraints: {constr_count}")

    # pop empty line
    lines.pop(0)
    
    # parse "c" vector
    c = [float(x) for x in lines.pop(0).split(" ")]
    print(f"c = {c}")
    assert len(c) == var_count

    # pop empty line
    lines.pop(0)

    # pop the "A" matrix
    A = []
    for i in range(constr_count):
        line = [float(x) for x in lines.pop(0).split(" ")]
        assert len(line) == var_count
        A.append(line)
    assert len(A) == constr_count 
    print(f"A = {A}")

    # pop empty line
    lines.pop(0)

    # parse the "b" vector
    b = [float(x) for x in lines.pop(0).split(" ")]
    assert len(b) == constr_count
    print(f"b = {b}")

    return c, A, b

def parse_problem_from_file(filepath: str) -> tuple[list[float], list[list[float]], list[float]]:
    contents = None
    with open(filepath, "r") as file:
        contents = file.read()
    
    return parse_problem(contents)


def main():
    parser = ArgumentParser(
        description = "Solve an integer linear programming problem."
    )
    parser.add_argument('file', help="path to file with the problem data")
    parser.add_argument('-c', '--check-solution', action="store_true", help="check solution against from the output of the HiGHS solver")

    args = parser.parse_args()

    c = None
    A = None
    b = None

    if args.file:
        c, A, b = parse_problem_from_file(args.file)

    if not c or not A or not b:
        print("Error: problem input was not provided!")
        exit(1)

    value, solution = bnb(c, A, b)
    if not solution:
        print("Result: problem is unfeasible!")
    else:
        print(f"Result: value={value}, solution={solution}")

    if args.check_solution:
        print("")
        print("Running problem against HiGHS")
        result = linprog(c, A, b, bounds=(0, None), integrality=[1]*len(c))
        print(result)
        if solution is not None:
            for x, x_expected in zip(solution, result.x):
                assert x == x_expected, f"Local solution ({solution}) doesn't match HiGHS ({result.x})!"
            print("")
        else:
            assert result.success == False
        print("No issues found (the solutions match)")


if __name__ == "__main__":
    main()
