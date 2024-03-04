import numpy as np

# point_21 = np.array([1070.142, -32.105, 19.636])
# point_31 = np.array([1040.137, -32.112, -31.857])

# sub = point_21 - point_31

# prev_prev = sub*sub

# prev = prev_prev[0]+prev_prev[1]+prev_prev[2]

# result = np.linalg.norm(point_21-point_31)

# print(result)

################################################

# offset = 29.639
# offset_hypo = offset/59.59

# result = np.rad2deg(np.arcsin(offset_hypo))
# print(result)

################################################

point = np.array([1070.458, -3.570, -31.96])
angle = 4.915

x, y, z = point
angle_rad = np.deg2rad(angle)
x_prime = x * np.cos(angle_rad) - y * np.sin(angle_rad)
y_prime = x * np.sin(angle_rad) + y * np.cos(angle_rad)
z_prime = z

print(x_prime)
print(y_prime)
print(z_prime)

