import freecad
import Part
import open3d as o3d
import numpy as np
from viewer import Viewer
from compute_correction import compute_correction
from compute_correction_non_orthogonal import compute_correction_non_orthogonal

# input_path = r"c:\Users\JorgeFernandes\Desktop\SW_Parts\simple_part\simple_weld_Step_ap214.STEP"
# mesh_filepath = r"c:\Users\JorgeFernandes\Desktop\SW_Parts\simple_part\simple_weld_Step_ap214.stl"

"""
with 6 touches, 2 in Y, Z and X we can compute rotation over vertical axis (here is the Y axis) and translation in XYZ
With 4 touches, 2 in Y and Z we can compute the rotation and translation over Vertical and longitudinal axis (but no lateral translation)
"""

use_six_touches = True

input_path = r"c:\Users\JorgeFernandes\Desktop\SW_Parts\corner_part\Part1.STEP"
mesh_filepath = r"c:\Users\JorgeFernandes\Desktop\SW_Parts\corner_part\Part1.STL"

shape = Part.Shape()
shape.read(input_path)

mesh = o3d.io.read_triangle_mesh(mesh_filepath)

if use_six_touches:
    x_translation = 10
    y_translation = 10
    z_translation = -10
    x_rotation = 0
    y_rotation = -0.1
    z_rotation = 0
else:
    x_translation = 0
    y_translation = 10
    z_translation = 10
    x_rotation = 0
    y_rotation = -0.1
    z_rotation = -0.1

# Apply rotation and translation 
mesh = mesh.translate((x_translation, y_translation, z_translation))
R = mesh.get_rotation_matrix_from_xyz((x_rotation, y_rotation, z_rotation))
mesh.rotate(R, center=(0, 0, 0))

triangle_mesh = o3d.t.geometry.TriangleMesh.from_legacy(mesh)
stl_mesh = o3d.t.geometry.RaycastingScene()
stl_mesh.add_triangles(triangle_mesh)

# edge_id = 11 # this should match the edge to be welded
edge_id = 1 # this should match the edge to be welded

weld_start = np.array(shape.Edges[edge_id].Vertexes[0].Point)
weld_end = np.array(shape.Edges[edge_id].Vertexes[1].Point)

viewer = Viewer()

#### Axis 1 ################################################
teo_sensing_point_1 = weld_start + np.array([20, 30, 0])
teo_sensing_point_2 = weld_start + np.array([75, 30, 0])

sensing_direction = np.array([0, 0, -1])
sensing_travel = 50

sensing_start_1 = teo_sensing_point_1 - sensing_direction * sensing_travel
tensor = np.append(sensing_start_1, sensing_direction)
rays_to_cast = o3d.core.Tensor(
    [tensor],
    dtype=o3d.core.Dtype.Float32,
)
rays_results = stl_mesh.cast_rays(rays_to_cast)
t_hits = rays_results["t_hit"].numpy()
real_sensing_point_1 = sensing_start_1 + sensing_direction * t_hits[0]

sensing_start_2 = teo_sensing_point_2 - sensing_direction * sensing_travel
tensor = np.append(sensing_start_2, sensing_direction)
rays_to_cast = o3d.core.Tensor(
    [tensor],
    dtype=o3d.core.Dtype.Float32,
)
rays_results = stl_mesh.cast_rays(rays_to_cast)
t_hits = rays_results["t_hit"].numpy()
real_sensing_point_2 = sensing_start_2 + sensing_direction * t_hits[0]

_, _, rotation_matrix_y, translation_matrix_y = compute_correction(
    weld_start,
    weld_end,
    teo_sensing_point_1,
    real_sensing_point_1,
    teo_sensing_point_2,
    real_sensing_point_2,
    axis="y",
)

# _, _, rotation_matrix_y, translation_matrix_y = compute_correction_non_orthogonal(
#     weld_start,
#     weld_end,
#     teo_sensing_point_1,
#     real_sensing_point_1,
#     sensing_start_1,
#     teo_sensing_point_2,
#     real_sensing_point_2,
#     axis="y",
# )

viewer.draw_sensing_arrows(
    sensing_start_1, 
    sensing_start_2, 
    sensing_direction, 
    real_sensing_point_1, 
    real_sensing_point_2,
)

# ### Axis 2 ################################################
teo_sensing_point_1 = weld_start + np.array([20, 0, 30])
teo_sensing_point_2 = weld_start + np.array([75, 0, 30])

sensing_direction = np.array([0, -1, 0])
sensing_travel = 50

sensing_start_1 = teo_sensing_point_1 - sensing_direction * sensing_travel
tensor = np.append(sensing_start_1, sensing_direction)
rays_to_cast = o3d.core.Tensor(
    [tensor],
    dtype=o3d.core.Dtype.Float32,
)
rays_results = stl_mesh.cast_rays(rays_to_cast)
t_hits = rays_results["t_hit"].numpy()
real_sensing_point_1 = sensing_start_1 + sensing_direction * t_hits[0]

sensing_start_2 = teo_sensing_point_2 - sensing_direction * sensing_travel
tensor = np.append(sensing_start_2, sensing_direction)
rays_to_cast = o3d.core.Tensor(
    [tensor],
    dtype=o3d.core.Dtype.Float32,
)
rays_results = stl_mesh.cast_rays(rays_to_cast)
t_hits = rays_results["t_hit"].numpy()
real_sensing_point_2 = sensing_start_2 + sensing_direction * t_hits[0]

_, _, rotation_matrix_z, translation_matrix_z = compute_correction(
    weld_start,
    weld_end,
    teo_sensing_point_1,
    real_sensing_point_1,
    teo_sensing_point_2,
    real_sensing_point_2,
    axis="z",
)

# _, _, rotation_matrix_z, translation_matrix_z = compute_correction_non_orthogonal(
#     weld_start,
#     weld_end,
#     teo_sensing_point_1,
#     real_sensing_point_1,
#     sensing_start_1,
#     teo_sensing_point_2,
#     real_sensing_point_2,
#     axis="z" # axis of rotation...
# )

viewer.draw_sensing_arrows(
    sensing_start_1, 
    sensing_start_2, 
    sensing_direction, 
    real_sensing_point_1, 
    real_sensing_point_2,
)

if use_six_touches:
    # ### Axis 3 ################################################
    teo_sensing_point_1 = weld_end + np.array([0, 50, 20])
    teo_sensing_point_2 = weld_end + np.array([0, 50, 50])

    sensing_direction = np.array([1, 0, 0])
    sensing_travel = 50

    sensing_start_1 = teo_sensing_point_1 - sensing_direction * sensing_travel
    tensor = np.append(sensing_start_1, sensing_direction)
    rays_to_cast = o3d.core.Tensor(
        [tensor],
        dtype=o3d.core.Dtype.Float32,
    )
    rays_results = stl_mesh.cast_rays(rays_to_cast)
    t_hits = rays_results["t_hit"].numpy()
    real_sensing_point_1 = sensing_start_1 + sensing_direction * t_hits[0]

    sensing_start_2 = teo_sensing_point_2 - sensing_direction * sensing_travel
    tensor = np.append(sensing_start_2, sensing_direction)
    rays_to_cast = o3d.core.Tensor(
        [tensor],
        dtype=o3d.core.Dtype.Float32,
    )
    rays_results = stl_mesh.cast_rays(rays_to_cast)
    t_hits = rays_results["t_hit"].numpy()
    real_sensing_point_2 = sensing_start_2 + sensing_direction * t_hits[0]

    _, _, _, translation_matrix_x = compute_correction(
        weld_start,
        weld_end,
        teo_sensing_point_1,
        real_sensing_point_1,
        teo_sensing_point_2,
        real_sensing_point_2,
        axis="x",
    )

    # _, _, _, translation_matrix_x = compute_correction_non_orthogonal(
    #     weld_start,
    #     weld_end,
    #     teo_sensing_point_1,
    #     real_sensing_point_1,
    #     sensing_start_1,
    #     teo_sensing_point_2,
    #     real_sensing_point_2,
    #     axis="x" # axis of rotation...
    # )

    viewer.draw_sensing_arrows(
        sensing_start_1, 
        sensing_start_2, 
        sensing_direction, 
        real_sensing_point_1, 
        real_sensing_point_2,
    )


weld_start_homogeneous = np.append(weld_start, 1)
weld_end_homogeneous = np.append(weld_end, 1)

weld_start_corrected = np.dot(translation_matrix_z, weld_start_homogeneous)
weld_end_corrected = np.dot(translation_matrix_z, weld_end_homogeneous)

weld_start_corrected = np.dot(translation_matrix_y, weld_start_corrected)
weld_end_corrected = np.dot(translation_matrix_y, weld_end_corrected)


if use_six_touches:
    weld_start_corrected = np.dot(translation_matrix_x, weld_start_corrected)
    weld_end_corrected = np.dot(translation_matrix_x, weld_end_corrected)
    
    # weld_start_corrected = np.dot(rotation_matrix_x, weld_start_corrected)
    # weld_end_corrected = np.dot(rotation_matrix_x, weld_end_corrected)

weld_start_corrected = np.dot(rotation_matrix_z, weld_start_corrected)
weld_end_corrected = np.dot(rotation_matrix_z, weld_end_corrected)

weld_start_corrected = np.dot(rotation_matrix_y, weld_start_corrected)
weld_end_corrected = np.dot(rotation_matrix_y, weld_end_corrected)


print(f"weldment start point: {weld_start}")
print(f"weldment end point: {weld_end}")
print(f"Corrected start point: {weld_start_corrected[:3]}")
print(f"Corrected end point: {weld_end_corrected[:3]}")

viewer.draw_weldment_points(
    mesh,
    weld_start,
    weld_end,
    weld_start_corrected,
    weld_end_corrected,
    mesh_filepath,
    wireframe=False,
    draw_original=True
)
