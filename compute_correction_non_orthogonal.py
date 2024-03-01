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

def compute_rotation_matrix(axis, theta):
    axis = normalize_vector(axis)
    K = np.array([[0, -axis[2], axis[1]],
                  [axis[2], 0, -axis[0]],
                  [-axis[1], axis[0], 0]])
    outer_product = np.outer(axis, axis)
    R = np.cos(theta) * np.eye(3) + (1 - np.cos(theta)) * outer_product - np.sin(theta) * K
    return R

def compute_correction_non_orthogonal(weld_start, weld_end, teo_sensing_point_1, real_sensing_point_1, sensing_start_1, teo_sensing_point_2, real_sensing_point_2, axis):

    offset_1 = real_sensing_point_1 - teo_sensing_point_1
    offset_2 = real_sensing_point_2 - teo_sensing_point_2

    offset_between_points = offset_2 - offset_1
    hypotenuse = np.linalg.norm(real_sensing_point_2 - real_sensing_point_1)
    
    # if axis == "z":
    #     angle = np.arcsin(offset_between_points[2] / hypotenuse) * 180 / np.pi
    # elif axis== "y":
    #     angle = np.arcsin(offset_between_points[1] / hypotenuse) * 180 / np.pi

    angle = np.arcsin(max(offset_between_points, key=abs)/hypotenuse)*180/np.pi

    print(f"Angle deviation on part for axis {axis}: {angle}")

    normalized_weldment_direction = normalize_vector(calculate_vector_direction(weld_start,weld_end))
    # sensing_direction = np.array([0, 0, -1])
    # sensing_travel = 50
    # sensing_start_1 = teo_sensing_point_1 - sensing_direction * sensing_travel
    normalized_sensing_direction = normalize_vector(calculate_vector_direction(sensing_start_1,teo_sensing_point_1))
    
    if axis in {"y", "z"}:
        rotation_vector = np.cross(normalized_weldment_direction, normalized_sensing_direction)
    elif axis == "x":
        pass
        # must use the direction of the sensing in -Z




    rot_matrix = compute_rotation_matrix(rotation_vector, np.deg2rad(angle))

    # # Apply rotation
    # if axis == "x":
    #     rotation_matrix = rotate_y(angle)
    # elif axis == "y":
    #     rotation_matrix = rotate_y(-angle)
    # elif axis == "z":
    #     rotation_matrix = rotate_z(angle)

    rotation_matrix_homogeneous = np.eye(4)
    rotation_matrix_homogeneous[:3, :3] = rot_matrix[:3, :3]

    # rotate point to original rotation in order to compute translation
    inv_rotation_matrix = np.linalg.inv(rotation_matrix_homogeneous)
    unrotated_real_sensing_point_1 = np.dot(inv_rotation_matrix, np.append(real_sensing_point_1, 1))[:3]

    displacement = unrotated_real_sensing_point_1-teo_sensing_point_1
    
    if axis == "y":
        z_displacement = displacement[2]
        print(f"displacement in z: {z_displacement}")
        translation_vector = [0, 0, z_displacement]
    elif axis == "z":
        y_displacement = displacement[1]
        print(f"displacement in y: {y_displacement}")
        translation_vector = [0, y_displacement, 0]
    elif axis == "x":
        x_displacement = displacement[0]
        print(f"displacement in x: {x_displacement}")
        translation_vector = [x_displacement, 0, 0]
    
    translation_matrix_homogeneous = np.eye(4)
    translation_matrix_homogeneous[:3, 3] = translation_vector

    # Apply transformations to weld points
    weld_start_homogeneous = np.append(weld_start, 1)
    weld_end_homogeneous = np.append(weld_end, 1)

    weld_start_corrected = np.dot(translation_matrix_homogeneous, weld_start_homogeneous)
    weld_end_corrected = np.dot(translation_matrix_homogeneous, weld_end_homogeneous)

    weld_start_corrected = np.dot(rotation_matrix_homogeneous, weld_start_corrected)[:3]
    weld_end_corrected = np.dot(rotation_matrix_homogeneous, weld_end_corrected)[:3]

    # print(f"weldment start point: {weld_start}")
    # print(f"weldment end point: {weld_end}")

    # print(f"Corrected start point: {weld_start_corrected}")
    # print(f"Corrected end point: {weld_end_corrected}")

    return weld_start_corrected, weld_end_corrected, rotation_matrix_homogeneous, translation_matrix_homogeneous