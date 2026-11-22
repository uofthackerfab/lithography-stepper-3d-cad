"""Render four unlabelled views of the checked-in public assembly.

uv run --no-project --python 3.12 --with pyvista --with trimesh python cad/render_gallery.py
"""
from collections import defaultdict
from pathlib import Path

import numpy as np
import pyvista as pv
import trimesh

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "img" / "gallery"


def load_meshes():
    scene = trimesh.load_scene(ROOT / "assembly/public/stepper.glb")
    groups = defaultdict(list)
    for node in scene.graph.nodes_geometry:
        transform, key = scene.graph[node]
        mesh = scene.geometry[key].copy()
        mesh.apply_transform(transform)
        colour = tuple(mesh.visual.material.baseColorFactor[:3])
        groups[colour].append(mesh)

    result = []
    for colour, pieces in groups.items():
        mesh = trimesh.util.concatenate(pieces)
        # GLB is in metres, Y up. Return to the CAD's millimetres, Z up.
        points = mesh.vertices[:, [0, 2, 1]] * [1000, -1000, 1000]
        faces = np.column_stack((np.full(len(mesh.faces), 3), mesh.faces))
        surface = pv.PolyData(points, faces).clean()
        surface = surface.compute_normals(split_vertices=True, feature_angle=35)
        # The GLB stores linear colour factors; VTK expects display colours.
        linear = np.array(colour) / 255
        rgb = np.where(linear <= 0.0031308, linear * 12.92,
                       1.055 * linear ** (1 / 2.4) - 0.055)
        result.append((surface, tuple(rgb)))
    return result


def render(meshes, name, position, focus, scale, dark=False):
    plotter = pv.Plotter(off_screen=True, window_size=(1920, 1200), lighting=None)
    plotter.set_background("#151d29" if dark else "#f4f3ef")
    for mesh, colour in meshes:
        plotter.add_mesh(mesh, color=colour, smooth_shading=True,
                         ambient=0.25 if dark else 0.2, diffuse=0.78,
                         specular=0.35, specular_power=40)
    ground = pv.Plane(center=(0, 0, -1), direction=(0, 0, 1),
                      i_size=30000, j_size=30000)
    plotter.add_mesh(ground, color="#151d29" if dark else "#f4f3ef",
                     ambient=0.45, diffuse=0.55)
    for location, intensity, colour in [
        ((-600, -500, 1000), 1.0, "#fff5e8"),
        ((550, -200, 550), 0.65, "#e4eeff"),
        ((50, 500, 800), 0.9, "#ffffff"),
    ]:
        plotter.add_light(pv.Light(position=location, focal_point=(0, 0, 230),
                                   color=colour, intensity=intensity,
                                   light_type="scene light"))
    plotter.enable_anti_aliasing("ssaa")
    plotter.enable_ssao(radius=35, bias=0.5, kernel_size=128, blur=True)
    plotter.camera_position = [position, focus, (0, 0, 1)]
    plotter.enable_parallel_projection()
    plotter.camera.parallel_scale = scale
    plotter.reset_camera_clipping_range()
    path = OUT / f"{name}.jpg"
    plotter.screenshot(path)
    plotter.close()
    print(path, flush=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    meshes = load_meshes()
    views = [
        ("stepper-studio", (-800, -1100, 800), (0, -80, 235), 340, False),
        ("stepper-reverse", (850, -850, 650), (0, -80, 235), 340, False),
        ("stepper-dark", (-800, -1100, 800), (0, -80, 235), 340, True),
        ("stepper-detail", (-550, -850, 450), (0, 5, 215), 155, False),
    ]
    for name, position, focus, scale, dark in views:
        render(meshes, name, position, focus, scale, dark)


if __name__ == "__main__":
    main()
