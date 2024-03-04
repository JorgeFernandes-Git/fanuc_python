import copy
import math
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

def rotate_point_around_z_axis(point, angle):
    x, y, z = point
    angle_rad = math.radians(angle)
    x_prime = x * math.cos(angle_rad) - y * math.sin(angle_rad)
    y_prime = x * math.sin(angle_rad) + y * math.cos(angle_rad)
    z_prime = z

    point_prime = [x_prime, y_prime, z_prime]
    
    return point_prime

def compute_correction(weld_start, weld_end, teo_sensing_point_1, real_sensing_point_1, teo_sensing_point_2, real_sensing_point_2, axis):

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


    # from viewer import Viewer
    # import open3d as o3d

    # mesh_filepath = r"c:\Users\JorgeFernandes\Desktop\SW_Parts\corner_part\Part1.STL"
    # mesh = o3d.io.read_triangle_mesh(mesh_filepath)

    # x_translation = 0
    # y_translation = 0
    # z_translation = 0
    # x_rotation = 0
    # y_rotation = 0
    # z_rotation = 0.1

    # mesh = mesh.translate((x_translation, y_translation, z_translation))
    # R = mesh.get_rotation_matrix_from_xyz((x_rotation, y_rotation, z_rotation))
    # mesh.rotate(R, center=(0, 0, 0))

    # test_1 = rotate_point_around_z_axis(weld_start, angle)
    # test_2 = rotate_point_around_z_axis(weld_end, angle)

    # viewer = Viewer()
    # viewer.draw_weldment_points(mesh,weld_start, weld_end, test_1, test_2, mesh_filepath, wireframe=False, draw_original=True)
    # exit()

    # Apply rotation
    if axis == "x":
        rotation_matrix = rotate_y(angle)
    elif axis == "y":
        rotation_matrix = rotate_y(-angle)
    elif axis == "z":
        rotation_matrix = rotate_z(angle)

    rotation_matrix_homogeneous = np.eye(4)
    rotation_matrix_homogeneous[:3, :3] = rotation_matrix[:3, :3]

    # rotate point to original rotation in order to compute translation
    inv_rotation_matrix = np.linalg.inv(rotation_matrix)
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