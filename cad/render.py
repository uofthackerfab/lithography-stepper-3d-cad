"""Render one picture of each STL file to docs/img/.

Run from the repository root:  uv run --with pyvista python -m cad.render
"""
from pathlib import Path

import pyvista as pv

ROOT = Path(__file__).resolve().parent.parent


def main():
    out = ROOT / "docs" / "img"
    out.mkdir(parents=True, exist_ok=True)
    for path in sorted((ROOT / "stl").glob("*.stl")):
        raw = pv.read(path).clean()
        edges = raw.extract_feature_edges(feature_angle=30, boundary_edges=False,
                                          non_manifold_edges=False, manifold_edges=False)
        mesh = raw.compute_normals(split_vertices=True, feature_angle=30, auto_orient_normals=True)
        p = pv.Plotter(off_screen=True, window_size=(1000, 750), lighting="three lights")
        p.set_background("white")
        p.add_mesh(mesh, color="#8fa3b8", smooth_shading=True, specular=0.25, specular_power=20,
                   ambient=0.18, diffuse=0.85)
        if edges.n_points:
            p.add_mesh(edges, color="#2b3440", line_width=2.0)
        p.enable_anti_aliasing("ssaa")
        p.enable_ssao(radius=mesh.length * 0.04, bias=0.5, kernel_size=128, blur=True)
        p.camera_position = "iso"
        p.camera.azimuth = -75
        p.camera.elevation = 8
        p.enable_parallel_projection()
        p.reset_camera()
        p.camera.zoom(0.95)
        p.screenshot(out / f"{path.stem}.png")
        p.close()
        print(path.stem)


if __name__ == "__main__":
    main()
