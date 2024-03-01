import numpy as np

point_21 = np.array([1070.142, -32.105, 19.636])
point_31 = np.array([1040.137, -32.112, -31.857])

sub = point_21 - point_31

prev_prev = sub*sub

prev = prev_prev[0]+prev_prev[1]+prev_prev[2]

result = np.linalg.norm(point_21-point_31)

print(result)