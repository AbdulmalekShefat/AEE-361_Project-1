import scipy.optimize
from Helper import *

I1 = I2 = I3 = 0
matrix = None
sigmas = []
index = 0


# -19,-4.7,6.45/-4.7,4.6,11.8/6.45,11.8,-8.3

def principle_stress_main():
    stress = stress_input()
    if stress is None:
        return
    stress = numpy.mat(stress).reshape(3, 3)
    stress_invariants(stress)


def stress_invariants(stress_matrix):
    global I1, I2, I3, matrix, sigmas
    matrix = stress_matrix
    I1 = compute_i1(stress_matrix)
    I2 = compute_i2(stress_matrix)
    I3 = compute_i3(stress_matrix)
    print("\nI's:")
    print("I-1: " + str(I1.round(3)))
    print("I-2: " + str(I2.round(3)))
    print("I-3: " + str(I3.round(3)))
    sigmas = principle_stresses()
    sigmas.sort()
    sigmas = sigmas[::-1]
    print("\nSigmas:")
    sigma1 = sigmas[0]
    sigma2 = sigmas[1]
    sigma3 = sigmas[2]
    print("σ-1: " + str(sigma1.round(3)))
    print("σ-2: " + str(sigma2.round(3)))
    print("σ-3: " + str(sigma3.round(3)))
    principle_dir = directions()
    plot_vectors(principle_dir)
    plot_mohrs_circle(sigmas)


def compute_i1(stress_matrix):
    return numpy.trace(stress_matrix)


def compute_i2(stress_matrix):
    part_1 = numpy.zeros((2, 2))
    part_2 = numpy.zeros((2, 2))
    part_3 = numpy.zeros((2, 2))
    # getting the first 2x2 matrix
    for i in range(0, 2):
        for j in range(0, 2):
            part_1[i, j] = stress_matrix[i, j]
    # getting the second 2x2 matrix
    for i in range(0, 3, 2):
        for j in range(0, 3, 2):
            part_2[i if i < 2 else i - 1, j if j < 2 else j - 1] = stress_matrix[i, j]
    # getting the third 2x2 matrix
    for i in range(1, 3):
        for j in range(1, 3):
            part_3[i - 1, j - 1] = stress_matrix[i, j]
    return numpy.linalg.det(part_1) + numpy.linalg.det(part_2) + numpy.linalg.det(part_3)


def compute_i3(stress_matrix):
    return numpy.linalg.det(stress_matrix)


def principle_stresses():
    coefficients = [1, -I1, +I2, -I3]
    return numpy.roots(coefficients)


def directions():
    direction = []
    global index
    index = 0
    guess = 0.5
    mGuess = scipy.array([guess, guess, guess])
    while index < 3:
        print("\nfor σ-" + str(index + 1))
        m = scipy.optimize.fsolve(direction_matrix, mGuess)
        print("n-x: " + str(m[0].round(4)))
        print("n-y: " + str(m[1].round(4)))
        print("n-z: " + str(m[2].round(4)))
        direction.append(m)
        index = index + 1
    return direction


def direction_matrix(ds):
    nx = ds[0]
    ny = ds[1]
    nz = ds[2]

    F = scipy.empty(3)
    F[0] = (matrix[0, 0] - sigmas[index]) * nx + matrix[0, 1] * ny + matrix[0, 2] * nz \
           + numpy.power(nx, 2) + numpy.power(ny, 2) + numpy.power(nz, 2) - 1
    F[1] = matrix[1, 0] * nx + (matrix[1, 1] - sigmas[index]) * ny + matrix[1, 2] * nz \
           + numpy.power(nx, 2) + numpy.power(ny, 2) + numpy.power(nz, 2) - 1
    F[2] = matrix[2, 0] * nx + matrix[2, 1] * ny + (matrix[2, 2] - sigmas[index]) * nz \
           + numpy.power(nx, 2) + numpy.power(ny, 2) + numpy.power(nz, 2) - 1

    return F
