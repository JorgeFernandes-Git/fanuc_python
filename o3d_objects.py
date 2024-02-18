import open3d as o3d
import numpy as np


"""
THIS FUNCTIONS ARE USED FOR DEBUG ONLY.
"""


def calculate_zy_rotation_for_arrow(vec):
    gamma = np.arctan2(vec[1], vec[0])
    Rz = np.array(
        [
            [np.cos(gamma), -np.sin(gamma), 0],
            [np.sin(gamma), np.cos(gamma), 0],
            [0, 0, 1],
        ]
    )

    vec = Rz.T @ vec

    beta = np.arctan2(vec[0], vec[2])
    Ry = np.array(
        [[np.cos(beta), 0, np.sin(beta)], [0, 1, 0], [-np.sin(beta), 0, np.cos(beta)]]
    )

    return Rz, Ry


def draw_arrow(
    end, origin=np.array([0, 0, 0]), color=[0, 0, 0], scale=1, cylinder_height=1
):
    assert not np.all(end == origin)
    direction = end - origin
    size = np.sqrt(np.sum(direction**2))

    Rz, Ry = calculate_zy_rotation_for_arrow(direction)
    mesh = o3d.geometry.TriangleMesh.create_arrow(
        cone_radius=size / 17.5 * scale,
        cone_height=size * 0.2 * scale,
        cylinder_radius=size / 30 * scale,
        cylinder_height=cylinder_height,
    )
    mesh.paint_uniform_color(color)
    mesh.rotate(Ry, center=np.array([0, 0, 0]))
    mesh.rotate(Rz, center=np.array([0, 0, 0]))
    mesh.translate(origin)

    return mesh


def draw_arrow_from_direction(
    direction, origin, color=[0, 0, 0], scale=1, cylinder_height=1
):
    size = np.sqrt(np.sum(direction**2))

    Rz, Ry = calculate_zy_rotation_for_arrow(direction)
    mesh = o3d.geometry.TriangleMesh.create_arrow(
        cone_radius=size / 17.5 * scale,
        cone_height=size * 0.2 * scale,
        cylinder_radius=size / 30 * scale,
        cylinder_height=cylinder_height,
    )
    mesh.paint_uniform_color(color)
    mesh.rotate(Ry, center=np.array([0, 0, 0]))
    mesh.rotate(Rz, center=np.array([0, 0, 0]))
    mesh.translate(origin)

    return mesh


def draw_sphere(center, radius, color=[1, 1, 1]):
    if len(center) > 3:
        center = center[:3]
    mesh = o3d.geometry.TriangleMesh.create_sphere(radius=radius)
    mesh.paint_uniform_color(color)
    mesh.translate(center)

    return mesh


def draw_cylinder(start, end, radius, length, color=[0.1, 0.9, 0.1]):
    assert not np.all(end == start)
    direction = end - start
    Rz, Ry = calculate_zy_rotation_for_arrow(direction)
    mesh = o3d.geometry.TriangleMesh.create_cylinder(radius=radius, height=length)
    mesh.compute_vertex_normals()
    mesh.paint_uniform_color(color)
    mesh.rotate(Ry, center=np.array([0, 0, 0]))
    mesh.rotate(Rz, center=np.array([0, 0, 0]))
    mesh.translate((start + end) / 2)

    return mesh


def draw_text(
    text,
    pos,
    direction=None,
    degree=0.0,
    density=10,
    font="/usr/share/fonts/truetype/freefont/FreeMono.ttf",
    font_size=10,
):
    """
    Generate a 3D text point cloud used for visualization.
    :param text: content of the text
    :param pos: 3D xyz position of the text upper left corner
    :param direction: 3D normalized direction of where the text faces
    :param degree: in plane rotation of text
    :param font: Name of the font - change it according to your system
    :param font_size: size of the font
    :return: o3d.geoemtry.PointCloud object
    """
    if direction is None:
        direction = (0.0, 0.0, 1.0)

    from PIL import Image, ImageFont, ImageDraw
    from pyquaternion import Quaternion

    # font_obj = ImageFont.truetype(font, font_size)
    font_obj = ImageFont.truetype(font, font_size * density)
    font_dim = font_obj.getsize(text)

    img = Image.new("RGB", font_dim, color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), text, font=font_obj, fill=(0, 0, 0))
    img = np.asarray(img)
    img_mask = img[:, :, 0] < 128
    indices = np.indices([*img.shape[0:2], 1])[:, img_mask, 0].reshape(3, -1).T

    pcd = o3d.geometry.PointCloud()
    pcd.colors = o3d.utility.Vector3dVector(img[img_mask, :].astype(float) / 255.0)
    # pcd.points = o3d.utility.Vector3dVector(indices / 100.0)
    pcd.points = o3d.utility.Vector3dVector(indices / 1000 / density)

    raxis = np.cross([0.0, 0.0, 1.0], direction)
    if np.linalg.norm(raxis) < 1e-6:
        raxis = (0.0, 0.0, 1.0)
    trans = (
        Quaternion(axis=raxis, radians=np.arccos(direction[2]))
        * Quaternion(axis=direction, degrees=degree)
    ).transformation_matrix
    trans[0:3, 3] = np.asarray(pos)
    pcd.transform(trans)

    return pcd


def draw_box(point, color, width=0.001, height=0.001, depth=0.001):
    x, y, z = point
    mesh = o3d.geometry.TriangleMesh.create_box(width=width, height=height, depth=depth)
    mesh.paint_uniform_color(color)
    mesh = mesh.translate((x - width / 2, y - height / 2, z - depth / 2))

    return mesh


if __name__ == "__main__":
    # vis = o3d.visualization.Visualizer()
    # vis.create_window()
    # vis.add_geometry(
    #     draw_arrow(
    #         origin=np.array([0, 0, 0]), end=np.array([1, 1, 1]), scale=1 / np.sqrt(3)
    #     )
    # )
    # vis.add_geometry(o3d.geometry.TriangleMesh().create_coordinate_frame())

    # vis.run()
    # vis.destroy_window()

    chessboard_coord = o3d.geometry.TriangleMesh.create_coordinate_frame(
        size=0.02, origin=[0, 0, 0]
    )
    pcd_10 = draw_text("Test-10mm", pos=[0, 0, 0.01], font_size=10, density=12)
    pcd_20 = draw_text("Test-20mm", pos=[0, 0, 0], font_size=20, density=2)
    o3d.visualization.draw_geometries([pcd_10, pcd_20, chessboard_coord])
