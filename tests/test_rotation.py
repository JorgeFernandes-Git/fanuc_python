import numpy as np

# THIS IS IGNORING THE ROTATION OF THE ROBOT (WPR)

# first point
teo_sensing_point_X1 = np.array([10, 5, 5])
real_sensing_point_X1 = np.array([11, 5, 5])


# second point
teo_sensing_point_X2 = np.array([10, 7, 7])
real_sensing_point_X2 = np.array([12, 7, 7])

offset_X1 = real_sensing_point_X1 - teo_sensing_point_X1
offset_X2 = real_sensing_point_X2 - teo_sensing_point_X2

# print(offset_X1)
# print(offset_X2)

offset_between_points = offset_X2 - offset_X1
# print(offset_between_points)

# Calculate average offset for rotation correction
average_offset = (offset_X1 + offset_X2) / 2  # this could be an idea??????

hypotenuse = np.linalg.norm(real_sensing_point_X2 - real_sensing_point_X1)

angle = np.arcsin(offset_between_points[0] / hypotenuse) * 180 / np.pi
# angle = np.arcsin(offset_X2[1] / hypotenuse) * 180 / np.pi

print(f"hypotenuse: {hypotenuse}")
print(f"angle: {angle} degrees.")

# teo start and end points of the weldment
weld_start = np.array([10, 2, 2])
weld_end = np.array([10, 10, 2])
print(f"weld_start: {weld_start}")
print(f"weld_end: {weld_end}")

weld_length = np.linalg.norm(weld_end - weld_start)
# print(f"weldment length: {weld_length}")

# corrected points of the weldment (approach not considering rotation using only one point of touch)
weld_start_corrected = weld_start
weld_end_corrected = weld_end
weld_start_corrected[0] = weld_start[0] + offset_X1[0]
weld_end_corrected[0] = weld_end[0] + offset_X1[0]
# print(f"weldment corrected start: {weld_start_corrected}")
# print(f"weldment corrected end: {weld_end_corrected}")

# correct the points using the rotation
# Corrected weldment points
rotation_matrix = np.array(
    [
        [np.cos(angle * np.pi / 180), -np.sin(angle * np.pi / 180), 0],
        [np.sin(angle * np.pi / 180), np.cos(angle * np.pi / 180), 0],
        [0, 0, 1],
    ]
)
weld_start_corrected = np.dot(rotation_matrix, weld_start)
weld_end_corrected = np.dot(rotation_matrix, weld_end)


print(f"weldment corrected start: {weld_start_corrected}")
print(f"weldment corrected end: {weld_end_corrected}")
