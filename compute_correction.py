import copy
import numpy as np

def normalize_vector(vector: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(vector)
    if norm == 0:
        return np.zeros_like(vector)
    return vector / norm

def calculate_vector_direction(
    start_point: np.ndarray, end_point: np.ndarray
) -> np.ndarray:
    direction_vector = end_point - start_point
    return direction_vector

def rotate_xyz(angle_x, angle_y, angle_z):
    rotation_x = np.array([
        [1, 0, 0],
        [0, np.cos(angle_x), -np.sin(angle_x)],
        [0, np.sin(angle_x), np.cos(angle_x)]
    ])
    rotation_y = np.array([
        [np.cos(angle_y), 0, np.sin(angle_y)],
        [0, 1, 0],
        [-np.sin(angle_y), 0, np.cos(angle_y)]
    ])
    rotation_z = np.array([
        [np.cos(angle_z), -np.sin(angle_z), 0],
        [np.sin(angle_z), np.cos(angle_z), 0],
        [0, 0, 1]
    ])

    # Combine the rotation matrices
    rotation_matrix = np.dot(rotation_z, np.dot(rotation_y, rotation_x))
    
    return rotation_matrix

def rotate_x(angle):
    rotation_matrix = np.array([
        [1, 0, 0, 0],
        [0, np.cos(np.radians(angle)), -np.sin(np.radians(angle)), 0],
        [0, np.sin(np.radians(angle)), np.cos(np.radians(angle)), 0],
        [0, 0, 0, 1]
    ])
    return rotation_matrix

def rotate_y(angle):
    rotation_matrix = np.array([
        [np.cos(np.radians(angle)), 0, np.sin(np.radians(angle)), 0],
        [0, 1, 0, 0],
        [-np.sin(np.radians(angle)), 0, np.cos(np.radians(angle)), 0],
        [0, 0, 0, 1]
    ])
    return rotation_matrix

def rotate_z(angle):
    rotation_matrix = np.array([
        [np.cos(angle * np.pi / 180), -np.sin(angle * np.pi / 180), 0, 0],
        [np.sin(angle * np.pi / 180), np.cos(angle * np.pi / 180), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    return rotation_matrix

def compute_correction(weld_start, weld_end, teo_sensing_point_1, real_sensing_point_1, teo_sensing_point_2, real_sensing_point_2, axis):

    offset_1 = real_sensing_point_1 - teo_sensing_point_1
    offset_2 = real_sensing_point_2 - teo_sensing_point_2

    # this only corrects translation, but not rotation...
    # weld_start_corrected = copy.deepcopy(weld_start)
    # weld_end_corrected = copy.deepcopy(weld_end)
    # weld_start_corrected[1] = weld_start[1] + offset_1[1]
    # weld_end_corrected[1] = weld_end[1] + offset_2[1]

    offset_between_points = offset_2 - offset_1
    hypotenuse = np.linalg.norm(real_sensing_point_2 - real_sensing_point_1)
    
    if axis == "y":
        angle = np.arcsin(offset_between_points[2] / hypotenuse) * 180 / np.pi
    elif axis== "z":
        angle = np.arcsin(offset_between_points[1] / hypotenuse) * 180 / np.pi

    print(f"Angle deviation on part for axis {axis}: {angle}")

    weld_length = np.linalg.norm(weld_end-weld_start)

    # Angle deviation on part for axis z: 11.23660241459323
    # [ 1.94860978 -9.80830872  0.        ]
    # Angle deviation on part for axis y: -11.459151798640878
    # [ 1.98669261 -0.          9.80066592]

    # compute frame
    y_vector = normalize_vector(calculate_vector_direction(real_sensing_point_1, real_sensing_point_2))
    if axis == "z":
        z_vector = [0,0,1]
    elif axis == "y":
        z_vector = [0,1,0]

    x_vector = np.cross(y_vector, z_vector)

    frame = np.column_stack([x_vector, y_vector, z_vector, np.zeros_like(x_vector)])
    frame = np.vstack([frame, [0, 0, 0, 1]])

    # Create a 4x4 identity matrix
    transformation_matrix = np.eye(4)

    # Apply rotation
    if axis == "x":
        rotation_matrix = rotate_x(angle)
    elif axis == "y":
        rotation_matrix = rotate_y(-angle)
    elif axis == "z":
        rotation_matrix = rotate_z(angle)

    transformation_matrix[:3, :3] = rotation_matrix[:3, :3]

    # Apply translation
    # Compute translation vector from teo sensing points to real sensing points
    # this is not working and its giving bad results

    # offset_mean = (offset_1 + offset_2)/2
    # translation_vector = 10*x_vector
    translation_vector = [0, 0, 0]  
    # rotated_translation_vector = np.dot(rotation_matrix[:3, :3], translation_vector)
    rotated_translation_vector = translation_vector
        
    print(rotated_translation_vector)

    transformation_matrix[:3, 3] = rotated_translation_vector 

    # Apply transformation to weld points
    weld_start_homogeneous = np.append(weld_start, 1)
    weld_end_homogeneous = np.append(weld_end, 1)

    weld_start_corrected = np.dot(transformation_matrix, weld_start_homogeneous)[:3]
    weld_end_corrected = np.dot(transformation_matrix, weld_end_homogeneous)[:3]

    # print(f"weldment start point: {weld_start}")
    # print(f"weldment end point: {weld_end}")

    # print(f"Corrected start point: {weld_start_corrected}")
    # print(f"Corrected end point: {weld_end_corrected}")

    return weld_start_corrected, weld_end_corrected, transformation_matrix