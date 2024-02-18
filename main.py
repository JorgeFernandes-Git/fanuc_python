import freecad
import Part
import open3d as o3d
import numpy as np
from viewer import Viewer
from compute_correction import compute_correction

input_path = r"c:\Users\jorge\OneDrive\Desktop\SW_parts\Weld_test.STEP"
mesh_filepath = r"c:\Users\jorge\OneDrive\Desktop\SW_parts\Weld_test.stl"

shape = Part.Shape()
shape.read(input_path)

mesh = o3d.io.read_triangle_mesh(mesh_filepath)
mesh = mesh.translate((0, 0, 0))
R = mesh.get_rotation_matrix_from_xyz((0, -0.2, 0))
mesh.rotate(R, center=(0, 0, 0))
triangle_mesh = o3d.t.geometry.TriangleMesh.from_legacy(mesh)
stl_mesh = o3d.t.geometry.RaycastingScene()
stl_mesh.add_triangles(triangle_mesh)

edge_id = 15
weld_start = np.array(shape.Edges[edge_id].Vertexes[0].Point)
weld_end = np.array(shape.Edges[edge_id].Vertexes[1].Point)

teo_sensing_point_1 = weld_start + np.array([0, 50, -50])
teo_sensing_point_2 = weld_start + np.array([0, 50, -120])

sensing_direction = np.array([1, 0, 0])
sensing_start_1 = teo_sensing_point_1 - sensing_direction * 100
tensor = np.append(sensing_start_1, sensing_direction)
rays_to_cast = o3d.core.Tensor(
    [tensor],
    dtype=o3d.core.Dtype.Float32,
)
rays_results = stl_mesh.cast_rays(rays_to_cast)
t_hits = rays_results["t_hit"].numpy()
real_sensing_point_1 = sensing_start_1 + sensing_direction * t_hits[0]

sensing_start_2 = teo_sensing_point_2 - sensing_direction * 100
tensor = np.append(sensing_start_2, sensing_direction)
rays_to_cast = o3d.core.Tensor(
    [tensor],
    dtype=o3d.core.Dtype.Float32,
)
rays_results = stl_mesh.cast_rays(rays_to_cast)
t_hits = rays_results["t_hit"].numpy()
real_sensing_point_2 = sensing_start_2 + sensing_direction * t_hits[0]

weld_start_corrected, weld_end_corrected = compute_correction(
    weld_start,
    weld_end,
    teo_sensing_point_1,
    real_sensing_point_1,
    teo_sensing_point_2,
    real_sensing_point_2,
)

viewer = Viewer()
viewer.draw_weldment_points(
    mesh,
    weld_start,
    weld_end,
    weld_start_corrected,
    weld_end_corrected,
    mesh_filepath,
    wireframe=False,
)
