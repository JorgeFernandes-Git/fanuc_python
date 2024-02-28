import numpy as np

# Define the translation matrix
translation_matrix = np.array([[1.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00],
                               [0.00000000e+00, 1.00000000e+00, 0.00000000e+00, 1.36156477e-06],
                               [0.00000000e+00, 0.00000000e+00, 1.00000000e+00, 0.00000000e+00],
                               [0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])

# Define the rotation matrix
rotation_matrix = np.array([[ 0.98006658, -0.19866933,  0.        ,  0.        ],
                            [ 0.19866933,  0.98006658,  0.        ,  0.        ],
                            [ 0.        ,  0.        ,  1.        ,  0.        ],
                            [ 0.        ,  0.        ,  0.        ,  1.        ]])

# Combine translation and rotation into a single transformation matrix
transformation_matrix = np.dot(translation_matrix, rotation_matrix)

# Now you have the combined transformation matrix
