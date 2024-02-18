import numpy as np
import o3d_objects
import open3d as o3d
from color import Color


class Viewer:
    def __init__(self) -> None:
        self.view = {
            "class_name": "ViewTrajectory",
            "interval": 29,
            "is_loop": False,
            "trajectory": [
                {
                    "boundingbox_max": [
                        0.10004454851150513,
                        0.06027492880821228,
                        0.099799647927284241,
                    ],
                    "boundingbox_min": [
                        -0.029000000000000001,
                        -0.039900962263345718,
                        -0.010503812693059444,
                    ],
                    "field_of_view": 60.0,
                    "front": [
                        -0.39525702166210391,
                        -0.75430526450899127,
                        0.5242093615730492,
                    ],
                    "lookat": [
                        0.046755475899682084,
                        -0.024125645104878003,
                        0.035053486918523134,
                    ],
                    "up": [
                        0.22628196232366699,
                        0.47313680141408621,
                        0.85143293375027385,
                    ],
                    "zoom": 0.84120000000000039,
                }
            ],
            "version_major": 1,
            "version_minor": 0,
        }

    def draw_weldment_points(
        self,
        mesh,
        start,
        end,
        start_corrected,
        end_corrected,
        path_to_stl_mesh,
        wireframe=False,
    ):
        entities = []

        entities.append(
            o3d.geometry.TriangleMesh().create_coordinate_frame(
                size=50, origin=np.array([0.0, 0.0, 0.0])
            )
        )

        # mesh = o3d.io.read_triangle_mesh(path_to_stl_mesh)

        if not wireframe:
            mesh.compute_vertex_normals()
            mesh.paint_uniform_color([0.6, 0.6, 0.6])
            entities.append(mesh)
        else:
            mesh_wireframe = o3d.geometry.LineSet.create_from_triangle_mesh(mesh)
            mesh_wireframe.paint_uniform_color([0.0, 0.7, 0.0])
            entities.append(mesh_wireframe)

        sphere_radius = 1
        # entities.append(
        #     o3d_objects.draw_sphere(start, sphere_radius, Color.BLACK.rgb())
        # )
        # entities.append(o3d_objects.draw_sphere(end, sphere_radius, Color.BLACK.rgb()))

        entities.append(
            o3d_objects.draw_sphere(start_corrected, sphere_radius, Color.BLACK.rgb())
        )
        entities.append(
            o3d_objects.draw_sphere(end_corrected, sphere_radius, Color.BLACK.rgb())
        )

        self.run_visualization(entities)

    def run_visualization(self, entities):
        o3d.visualization.draw_geometries(
            entities,
            window_name="visualization",
            zoom=self.view["trajectory"][0]["zoom"],
            front=self.view["trajectory"][0]["front"],
            lookat=self.view["trajectory"][0]["lookat"],
            up=self.view["trajectory"][0]["up"],
            point_show_normal=False,
        )
