import numpy as np


def rotate_x(angle):
    rotation_matrix = np.array(
        [
            [1, 0, 0],
            [0, np.cos(np.radians(angle)), -np.sin(np.radians(angle))],
            [0, np.sin(np.radians(angle)), np.cos(np.radians(angle))],
        ]
    )
    return rotation_matrix


def rotate_y(angle):
    rotation_matrix = np.array(
        [
            [np.cos(np.radians(angle)), 0, np.sin(np.radians(angle))],
            [0, 1, 0],
            [-np.sin(np.radians(angle)), 0, np.cos(np.radians(angle))],
        ]
    )
    return rotation_matrix


def rotate_z(angle):
    rotation_matrix = np.array(
        [
            [np.cos(angle * np.pi / 180), -np.sin(angle * np.pi / 180), 0],
            [np.sin(angle * np.pi / 180), np.cos(angle * np.pi / 180), 0],
            [0, 0, 1],
        ]
    )

    return rotation_matrix


def compute_correction(
    weld_start,
    weld_end,
    teo_sensing_point_1,
    real_sensing_point_1,
    teo_sensing_point_2,
    real_sensing_point_2,
):

    offset_1 = real_sensing_point_1 - teo_sensing_point_1
    offset_2 = real_sensing_point_2 - teo_sensing_point_2

    # this only corrects translation, but not rotation...
    # weld_start_corrected = weld_start
    # weld_end_corrected = weld_end
    # weld_start_corrected[0] = weld_start[0] + offset_1[0]
    # weld_end_corrected[0] = weld_end[0] + offset_1[0]

    offset_between_points = offset_2 - offset_1
    hypotenuse = np.linalg.norm(real_sensing_point_2 - real_sensing_point_1)
    angle = np.arcsin(offset_between_points[0] / hypotenuse) * 180 / np.pi

    print(f"angle: {angle}")

    # rotation_matrix = rotate_x(angle)
    rotation_matrix = rotate_y(-angle)
    # rotation_matrix = rotate_z(angle)

    weld_start_corrected = np.dot(rotation_matrix, weld_start)
    weld_end_corrected = np.dot(rotation_matrix, weld_end)

    print(weld_start)
    print(weld_end)

    print(weld_start_corrected)
    print(weld_end_corrected)

    return weld_start_corrected, weld_end_corrected
