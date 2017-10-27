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
    angles = numpy.mat(angles)

    print("\n##################### Calculating Vector transformation #####################")

    if 0 in angles:
        print('\nrotation about ' + get_axis(numpy.where(angles == 0)[1][0]))
        transformation_matrix = transformation_matrix_2d(angles)
    else:
        transformation_matrix = transformation_matrix_3d(angles)
    transformation_matrix_transpose = matrix_transpose(transformation_matrix)
    transformed_vector = matrix_multiplication(transformation_matrix_transpose, vector)

    print("\nTransformation Matrix:")
    print(numpy.around(transformation_matrix, 3))
    print("\nTransformed Vector:")
    print(numpy.around(transformed_vector, 3))

    plot_vectors([vector, transformed_vector], 'vector_transformation.png')
