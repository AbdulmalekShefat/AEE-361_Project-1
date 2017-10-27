from PrincipleStress import *


def stress_main_():
    principle_stress = principle_stresses_dialog()
    stress = stress_input()
    if stress is None:
        return
    stress = numpy.mat(stress).reshape(3, 3)

    angles = angle_input()
    if angles is None:
        return
    angles = numpy.mat(angles).reshape(1, 3)

    print("\n##################### Calculating Stress transformation #####################")

    if angles is not None and 0 in angles:
        print('\nRotation about (' + get_axis(numpy.where(angles == 0)[1][0]) + ')')
        transformation_matrix = transformation_matrix_2d(angles)
    else:
        transformation_matrix = transformation_matrix_3d(angles)

    transformation_matrix_transpose = matrix_transpose(transformation_matrix)
    transformed_stress = matrix_multiplication(matrix_multiplication(transformation_matrix_transpose,
                                                                     stress), transformation_matrix)

    print("\nTransformation Matrix:")
    print(transformation_matrix)

    print("\nTransformed Stress:")
    print(transformed_stress)

    if principle_stress:
        print("\n##################### Calculating Principle Stresses #####################")
        stress_invariants(stress)
