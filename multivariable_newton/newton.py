import numpy as np
from numpy.typing import NDArray 
from typing import Callable

# calculate the gradient (column vector with first partial derivatives
# as the entries)
def r(f: Callable[[NDArray], float], x: NDArray, h: float = 0.001) -> NDArray:
    shape = x.shape
    # check if it's a line (flat) vector
    if shape[0] != 1:
        raise ValueError("x is not a column vector")

    output = np.zeros(shape)
    for i in range(0, shape[1]):
        e = np.zeros(shape)
        e[0][i] = 1.0
        # calculate del f/del x_i
        pderiv = (f(x + h*e) - f(x))/h
        output[0][i] = pderiv

    return output

def main():
    def f(x):
        return x[0]*x[0] + x[1] * x[1]


if __name__ == "__main__":
    main()
