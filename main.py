import freecad
import Part
import open3d as o3d
import numpy as np
from viewer import Viewer
from compute_correction import compute_correction

input_path = r"c:\Users\JorgeFernandes\Desktop\SW_Parts\simple_part\simple_weld_Step_ap214.STEP"
mesh_filepath = r"c:\Users\JorgeFernandes\Desktop\SW_Parts\simple_part\simple_weld_Step_ap214.stl"

shape = Part.Shape()
shape.read(input_path)

mesh = o3d.io.read_triangle_mesh(mesh_filepath)

# Apply rotation and translation 
mesh = mesh.translate((0, 0, 0))
R = mesh.get_rotation_matrix_from_xyz((0, 0.2, 0.2))
mesh.rotate(R, center=(0, 0, 0))

triangle_mesh = o3d.t.geometry.TriangleMesh.from_legacy(mesh)
stl_mesh = o3d.t.geometry.RaycastingScene()
stl_mesh.add_triangles(triangle_mesh)

edge_id = 11
weld_start = np.array(shape.Edges[edge_id].Vertexes[0].Point)
weld_end = np.array(shape.Edges[edge_id].Vertexes[1].Point)

viewer = Viewer()

#### Axis 1 ################################################
teo_sensing_point_1 = weld_start + np.array([20, 0, -30])
teo_sensing_point_2 = weld_start + np.array([75, 0, -30])

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

_, _, transformation_matrix_z = compute_correction(
    weld_start,
    weld_end,
    teo_sensing_point_1,
    real_sensing_point_1,
    teo_sensing_point_2,
    real_sensing_point_2,
    axis="z",
)

viewer.draw_sensing_arrows(
    sensing_start_1, 
    sensing_start_2, 
    sensing_direction, 
    real_sensing_point_1, 
    real_sensing_point_2,
)

### Axis 2 ################################################
teo_sensing_point_1 = weld_start + np.array([20, 20, 0])
teo_sensing_point_2 = weld_start + np.array([75, 20, 0])

sensing_direction = np.array([0, 0, 1])
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

_, _, transformation_matrix_y = compute_correction(
    weld_start,
    weld_end,
    teo_sensing_point_1,
    real_sensing_point_1,
    teo_sensing_point_2,
    real_sensing_point_2,
    axis="y"
)

viewer.draw_sensing_arrows(
    sensing_start_1, 
    sensing_start_2, 
    sensing_direction, 
    real_sensing_point_1, 
    real_sensing_point_2,
)

weld_start_homogeneous = np.append(weld_start, 1)
weld_end_homogeneous = np.append(weld_end, 1)
weld_start_corrected = np.dot(transformation_matrix_y, np.dot(transformation_matrix_z, weld_start_homogeneous))[:3]
weld_end_corrected = np.dot(transformation_matrix_y, np.dot(transformation_matrix_z, weld_end_homogeneous))[:3]

print(f"weldment start point: {weld_start}")
print(f"weldment end point: {weld_end}")

print(f"Corrected start point: {weld_start_corrected}")
print(f"Corrected end point: {weld_end_corrected}")

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
