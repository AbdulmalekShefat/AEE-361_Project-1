import numpy
import scipy.optimize
import wx
import matplotlib as mpl

mpl.use('WXAgg')
import matplotlib.pyplot as plt
from matplotlib import patches
from mpl_toolkits.mplot3d import Axes3D

l1 = m2 = n3 = l2 = 0


# verification
def sum_of_array(array):
    i = 0
    for val in array:
        i += val
    return i


def occurrences(array, item):
    i = 0
    for j in array:
        if j == item:
            i = i + 1
    return i


def get_axis(i):
    if i == 0:
        return "x-axis"
    elif i == 1:
        return "y-axis"
    else:
        return "z-axis"


def valid_transformation_angles(a):
    if len(a) != 3:
        return False
    try:
        for n in a:
            float(n)
    except ValueError:
        return False
    a = [float(i) for i in a]
    if occurrences(a, 0) > 1:
        return False
    if 0 in a and (sum_of_array(a) / 2.0) not in a:
        return False
    return True


def valid_3x3_matrix(s):
    if len(s.split('/')) != 3:
        return False
    for r in s.split('/'):
        if len(r.split(',')) != 3:
            return False
        try:
            for c in r.split(','):
                float(c)
        except ValueError:
            return False
    return True


def valid_3d_vector(v):
    if len(v) != 3:
        return False
    try:
        for i in v:
            float(i)
    except ValueError:
        return False
    return True


# extra +needed calculations
def sign_convention(i, j):
    if i + j == 1:
        if i > j:
            return -1
        else:
            return 1
    else:
        if i > j:
            return 1
        else:
            return -1


def matrix_transpose(m):
    return numpy.transpose(m)


def matrix_multiplication(m, n):
    return numpy.dot(m, n)


# transformation matrices
def transformation_matrix_2d(angles):
    trans_matrix = numpy.zeros((3, 3))
    axis = numpy.where(angles == 0)[1][0]
    trans_matrix[axis, axis] = 1
    for i in range(0, 3):
        for j in range(0, 3):
            if i == axis or j == axis:
                continue
            if i == j:
                trans_matrix[i, j] = numpy.cos(numpy.deg2rad(angles[0, i]))
                continue
            trans_matrix[i, j] = numpy.cos(numpy.deg2rad(90 + (sign_convention(i, j) * angles[0, i])))

    return numpy.around(trans_matrix, decimals=4)


def transformation_matrix_3d(angles):
    global l1, l2, m2, n3
    l1 = numpy.cos(numpy.deg2rad(angles[0, 0]))
    m2 = numpy.cos(numpy.deg2rad(angles[0, 1]))
    n3 = numpy.cos(numpy.deg2rad(angles[0, 2]))
    l2 = numpy.cos(numpy.deg2rad(angles[0, 3]))
    print(l2)

    guess = (l1 + m2 + n3) / 6.

    guesses = scipy.array([guess, guess, guess, guess, guess])

    m = scipy.optimize.fsolve(directional_cosines, guesses)
    m = list(m)
    m.insert(0, l1)
    m.insert(1, l2)
    m.insert(4, m2)
    m.append(n3)

    return numpy.around(numpy.mat(m).reshape(3, 3), decimals=4)


def directional_cosines(m):
    l3 = m[0]
    m1 = m[1]
    m3 = m[2]
    n1 = m[3]
    n2 = m[4]

    F = scipy.empty(5)
    F[0] = (l1 * l1) + (m1 * m1) + (n1 * n1) - 1
    F[1] = (l1 * l2) + (m1 * m2) + (n1 * n2)
    F[2] = (l1 * l3) + (m1 * m3) + (n1 * n3)
    F[3] = (l2 * l2) + (m2 * m2) + (n2 * n2) - 1
    F[4] = (l2 * l3) + (m2 * m3) + (n2 * n3)
    # F[5] = (l3 * l3) + (m3 * m3) + (n3 * n3) - 1

    return F


# inputs

def stress_input():
    stress = [[], [], []]
    s = ask_dialog("Stress Input",
                   "enter the 3x3 stress matrix\nseparated by \',\' for new column and / for new row\nEx: (xx, "
                   "xy, xz / yx, yy, yz / zx, zy, zz)")
    if s is None:
        return

    while s == "" or not valid_3x3_matrix(s):
        s = ask_dialog("Stress Input",
                       "Enter a valid 3x3 stress matrix\n* columns separated by \',\' and rows separated by '/'\nEx: "
                       "(xx, xy, xz / yx, yy, yz / zx, zy, zz)")

    for r, row in enumerate(s.split('/')):
        for val in row.split(','):
            stress[r].append(float(val))

    return stress


def principle_stresses_dialog():
    dlg = wx.MessageDialog(None, "Do you want to obtain Principle Stresses?", 'Principle Stress',
                           wx.YES_NO | wx.ICON_QUESTION)
    result = dlg.ShowModal()
    return result == wx.ID_YES


def ask_dialog(title='AEE 361 Project', message=''):
    dlg = wx.TextEntryDialog(None, message, title)
    if dlg.ShowModal() == wx.ID_OK:
        result = str(dlg.GetValue()).replace(" ", "")
    else:
        result = None
    dlg.Destroy()
    return result


def angle_input():
    angles = []
    a = ask_dialog("Transformation Angles",
                   "enter the transformation angles (in degrees)\nseparated by \',\'\nEx: (angle(x, x'), angle(y, "
                   "y'), angle(z, z')")
    if a is None:
        return
    while a == "" or not valid_transformation_angles(a.split(',')):
        a = ask_dialog("Transformation Angles",
                       "enter a valid transformation angles (in degrees)\nseparated by \',\'\nEx: (angle(x, x'), "
                       "angle(y, y'), angle(z, z')")
    for row in a.split(","):
        angles.append(float(row))
    return angles


def l2_input():
    a = ask_dialog("Transformation Angles",
                   "enter the angle (in degrees) between (x, y')")
    if a is None:
        return
    while not float(a):
        a = ask_dialog("Transformation Angles",
                       "enter the angle (in degrees) between (x, y')")

    return float(a)


def vector_input():
    vector = []
    v = ask_dialog("Vector Coordinates", "enter the vector coordinates\nseparated by \',\'\nEx: (x, y, z)")
    if v is None:
        return None
    while v == "" or not valid_3d_vector(v.split(",")):
        v = ask_dialog("Vector Coordinates", "enter a valid 3-D vector coordinates\nseparated by \',\'\nEx: (x, y, z)")
    for row in v.split(","):
        vector.append(float(row))
    return vector


def plot_mohrs_circle(principle_stresses):
    sigma1 = principle_stresses[0]
    sigma2 = principle_stresses[1]
    sigma3 = principle_stresses[2]

    radius1 = (sigma1 - sigma2) / 2.0
    center1 = (sigma1 + sigma2) / 2.0

    radius2 = (sigma2 - sigma3) / 2.0
    center2 = (sigma2 + sigma3) / 2.0

    radius3 = (sigma1 - sigma3) / 2.0
    center3 = (sigma1 + sigma3) / 2.0

    fig1 = plt.figure("Mohr\'s Circle")
    ax = fig1.add_subplot(111, aspect='equal')
    ax.add_patch(patches.Circle((center1, 0),
                                radius=radius1,
                                color='r', linewidth=1, fill=False))
    ax.add_patch(patches.Circle((center2, 0),
                                radius=radius2,
                                color='g', linewidth=1, fill=False))
    ax.add_patch(patches.Circle((center3, 0),
                                radius=radius3,
                                color='b', linewidth=1, fill=False))

    markers_on = [sigma1, sigma2, sigma3]
    n = ['Sigma-1: ', 'Sigma-2: ', 'Sigma-3: ']
    for i, txt in enumerate(n):
        ax.annotate(txt + str(markers_on[i].round(3)), (markers_on[i], 0))
        plt.scatter(markers_on[i], 0, c='k')

    ax.grid(True)
    ax.autoscale_view()
    fig1.savefig('mohr\'s_circle.png')
    plt.show()


def plot_vectors(principle_dir, filename="principle_directions.png"):
    vectors = numpy.array(principle_dir)
    fig = plt.figure('Principle Directions')
    ax = fig.gca(projection='3d')
    colors = ['g', 'b', 'r']
    ax.set_xlim3d(-4, 4)
    ax.set_ylim3d(-4, 4)
    ax.set_zlim3d(-4, 4)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    for (i, vector) in enumerate(vectors):
        ax.quiver(0, 0, 0, vector[0], vector[1], vector[2], length=4, normalize=True, color=colors[i])
    ax.autoscale_view()
    fig.savefig(filename)
    plt.show(block=False)
