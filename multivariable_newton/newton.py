import numpy as np
from numpy import matmul
from numpy.linalg import inv, eig
from numpy.typing import NDArray 
from typing import Callable

def newton(f: Callable[[NDArray], float],
           r: Callable[[NDArray], NDArray],
           J: Callable[[NDArray], NDArray],
           x_0: NDArray, max_iterations: int = 50,
           epsilon: float = 1e-03) -> NDArray:
    if r(x_0).shape[1] != 1 or r(x_0).shape[0] != J(x_0).shape[0] or r(x_0).shape[0] != J(x_0).shape[1]:
        raise ValueError("invalid dimensions for r and J")
    x = x_0
    iteration = 0
    print(f"initial guess: {x.T}")
    while iteration < max_iterations:
        # print(f"------ iteration {iteration} ------")
        # print(f"r({x}): {r(x)}")
        # print(f"J({x}): {J(x)}")
        if np.abs(r(x).max()) <= epsilon:
            break
        delta_x = -1 * matmul(inv(J(x)), r(x))
        x += delta_x
        iteration += 1
    print(f"stopped after iteration {iteration}")
    print(f"result: point x={x.T} yields f(x)={f(x)}")
    eigenvals, eigenvecs = eig(J(x))
    print(f"eigenvalues of J: {eigenvals}")
    return x


def q1():
    def f(x):
        x = x[0][0]
        return 0.05*(x-4)**4 + 10*x**2 + 79*np.sin(0.5*x**2)

    def r(x):
        x = x[0][0]
        return np.array([
            [0.2*(x-4)**3 + 20*x + 79*x*np.cos(0.5*x**2)]
        ])

    def J(x):
        x = x[0][0]
        return np.array([
            [0.6*(x-4)**2 + 20 + 79*np.cos(0.5*x**2) - 79*(x**2)*np.sin(0.5*x**2)]
        ])

    initial_guesses = [
        np.array([[-5.0]]),
        np.array([[1.0]]),
        np.array([[5.0]]),
    ]

    for x_0 in initial_guesses:
        result = newton(f, r, J, x_0)
        print("------------")

def q2():
    def f(x):
        x1 = x[0][0]
        x2 = x[1][0]
        x3 = x[2][0]
        return 6*x1**4 + 3*x2**4 + 10*x3**4 + 20*np.sin(x1+x2+x3)

    def r(x):
        x1 = x[0][0]
        x2 = x[1][0]
        x3 = x[2][0]
        return np.array([
            [24*x1**3 + 20*np.cos(x1+x2+x3)],
            [12*x2**3 + 20*np.cos(x1+x2+x3)],
            [40*x3**3 + 20*np.cos(x1+x2+x3)],
        ])

    def J(x):
        x1 = x[0][0]
        x2 = x[1][0]
        x3 = x[2][0]
        return np.array([
            [72*x1**2 - 20*np.sin(x1+x2+x3), -20*np.sin(x1+x2+x3), -20*np.sin(x1+x2+x3)],
            [-20*np.sin(x1+x2+x3), 36*x2**2 - 20*np.sin(x1+x2+x3), -20*np.sin(x1+x2+x3)],
            [-20*np.sin(x1+x2+x3), -20*np.sin(x1+x2+x3), 120*x3**2 - 20*np.sin(x1+x2+x3)],
        ])

    initial_guesses = [
        np.array([[-1.0, 5.0, -5.0]]).T,
        np.array([[1.0, 3.0, -2.0]]).T,
        np.array([[5.0, 1.0, 5.0]]).T,
    ]

    for x_0 in initial_guesses:
        result = newton(f, r, J, x_0)
        print("------------")

def main():
    q2()

if __name__ == "__main__":
    main()
