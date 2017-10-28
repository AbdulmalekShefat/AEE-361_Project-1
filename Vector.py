from Helper import *
import numpy


def vector_main_():
    vector = vector_input()
    if vector is None:
        return
    vector = numpy.mat(vector).reshape(3, 1)
    angles = angle_input()
    if angles is None:
        return
    angles_mat = numpy.mat(angles)
    print(angles_mat)

    print("\n##################### Calculating Vector transformation #####################")

    if 0 in angles_mat:
        print('\nrotation about ' + get_axis(numpy.where(angles_mat == 0)[1][0]))
        transformation_matrix = transformation_matrix_2d(angles_mat)
    else:
        l2 = l2_input()
        angles.append(l2)
        angles_mat = numpy.mat(angles)
        print(angles_mat)
        transformation_matrix = transformation_matrix_3d(angles_mat)
    transformation_matrix_transpose = matrix_transpose(transformation_matrix)
    transformed_vector = matrix_multiplication(transformation_matrix_transpose, vector)

    print("\nTransformation Matrix:")
    print(numpy.around(transformation_matrix, 4))
    print("\nTransformed Vector:")
    print(numpy.around(transformed_vector, 4))

    plot_vectors([vector, transformed_vector], 'vector_transformation.png')
