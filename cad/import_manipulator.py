"""Convert the CAD of the Open Micro-Manipulator to cad/data/manipulator.brep. FreeCAD is not necessary.

Run this only if the source CAD changes:

    uv run python -m cad.import_manipulator <MicroManipulatorStepper folder> <demoStandV1.stl>

Sources (MIT licence, see cad/data/LICENSE-MicroManipulatorStepper):
- github.com/0x23/MicroManipulatorStepper, construction/micro_manipulator/*.FCStd
- github.com/koalazak/MicroManipulatorStepper, branch stl-extras, demoStandV1.stl

An FCStd file is a zip file. It contains Document.xml (objects, links, positions) and one
BREP file for each shape. This script follows the links of Assembly_MicroManipulator.FCStd.
Coordinates: origin of the base block, as in the FreeCAD assembly.
"""
import sys
import tempfile
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

from build123d import Compound, Shape, export_brep
from OCP.BRep import BRep_Builder
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeSolid, BRepBuilderAPI_Sewing
from OCP.BRepTools import BRepTools
from OCP.gp import gp_Quaternion, gp_Trsf, gp_Vec
from OCP.ShapeUpgrade import ShapeUpgrade_UnifySameDomain
from OCP.StlAPI import StlAPI_Reader
from OCP.TopLoc import TopLoc_Location
from OCP.TopoDS import TopoDS, TopoDS_Shape

DATA = Path(__file__).resolve().parent / "data"
CONTAINERS = ("Assembly::AssemblyObject", "Assembly::AssemblyLink", "App::Part", "App::DocumentObjectGroup")
GROUPS = [("MotorMount", "motor mount"), ("StepperMotor", "motor"), ("MotorHorn", "motor horn"),
          ("LinkageUnit", "linkage"), ("Encoder", "encoder"), ("MT68", "encoder")]


class Reader:
    def __init__(self, folder):
        self.folder, self.docs, self.seen = Path(folder), {}, set()

    def doc(self, name):
        """Return ({object: type}, {object: {property: xml element}}) of one FCStd file."""
        if name not in self.docs:
            root = ET.parse(self.folder / name / "Document.xml").getroot()
            types = {o.get("name"): o.get("type") for o in root.find("Objects")}
            props = {o.get("name"): {p.get("name"): (list(p) or [None])[0] for p in o.find("Properties")}
                     for o in root.find("ObjectData")}
            self.docs[name] = (types, props)
        return self.docs[name]

    def label(self, d, o):
        e = self.doc(d)[1][o].get("Label")
        return e.get("value") if e is not None else o

    def target(self, d, o):
        """Follow App::Link objects to the object that has the shape."""
        while self.doc(d)[0][o] == "App::Link":
            e = self.doc(d)[1][o]["LinkedObject"]
            if e.get("file"):
                d, o = e.get("file").replace(".FCStd", ""), e.get("name")
            else:
                o = e.get("value") or e.get("name")
        return d, o

    def shape(self, d, o):
        types, props = self.doc(d)
        if types[o] == "PartDesign::Body":
            o = props[o]["Tip"].get("value")
        e = props[o].get("Shape")
        if e is None or not e.get("file"):
            return None
        s = TopoDS_Shape()
        BRepTools.Read_s(s, str(self.folder / d / e.get("file")), BRep_Builder())
        s.Location(TopLoc_Location())
        return s

    def walk(self, d, o, trsf, path, out, own=True):
        """Append (label path, positioned shape) of each part below object `o` to `out`."""
        types, props = self.doc(d)
        kind, p = types.get(o) or "", props.get(o, {})
        v = trsf.TranslationPart()
        key = (d, o, round(v.X(), 3), round(v.Y(), 3), round(v.Z(), 3))
        if key in self.seen:                            # FreeCAD lists a part in a group and in its parent
            return
        self.seen.add(key)
        if kind in CONTAINERS:
            t = trsf.Multiplied(placement(p.get("Placement"))) if own else trsf
            for e in (p["Group"] if p.get("Group") is not None else []):
                self.walk(d, e.get("value"), t, path + [self.label(d, o)], out)
        elif kind == "App::Link":
            t = trsf.Multiplied(placement(p.get("LinkPlacement")))
            d2, o2 = self.target(d, o)
            if self.doc(d2)[0][o2] in CONTAINERS:       # a link ignores the position of its target
                self.walk(d2, o2, t, path + [self.label(d, o)], out, own=False)
            elif (s := self.shape(d2, o2)) is not None:
                out.append((path + [self.label(d, o)], s.Moved(TopLoc_Location(t))))
        elif ((kind.startswith("Part::") and "Datum" not in kind) or kind == "PartDesign::Body") \
                and (s := self.shape(d, o)) is not None:
            out.append((path + [self.label(d, o)], s.Moved(TopLoc_Location(trsf.Multiplied(placement(p.get("Placement")))))))


def placement(e):
    t = gp_Trsf()
    if e is not None:
        a = {k: float(v) for k, v in e.attrib.items()}
        t.SetRotation(gp_Quaternion(a["Q0"], a["Q1"], a["Q2"], a["Q3"]))
        t.SetTranslationPart(gp_Vec(a["Px"], a["Py"], a["Pz"]))
    return t


def group(path):
    """Name of the assembly part that the FreeCAD part `path` belongs to."""
    if "Screw" in path[-1] or "Pin" in path[-1]:
        return "screws and pins"
    if path[1].startswith("Actuator"):
        for key, name in GROUPS:
            if any(key in p for p in path[2:]):
                return f"actuator {path[1][-1]} {name}"
    return {"BaseBlock": "base block", "Endeffector": "end effector"}[path[1]]


def stl_solid(path):
    """Read an STL file. Return one solid with merged flat faces."""
    mesh = TopoDS_Shape()
    StlAPI_Reader().Read(mesh, str(path))
    sew = BRepBuilderAPI_Sewing(1e-3)
    sew.Add(mesh)
    sew.Perform()
    solid = BRepBuilderAPI_MakeSolid(TopoDS.Shell(sew.SewedShape())).Solid()
    unify = ShapeUpgrade_UnifySameDomain(solid, True, True, False)
    unify.Build()
    return unify.Shape()


def main(repo, stand):
    with tempfile.TemporaryDirectory() as tmp:
        for f in (Path(repo) / "construction" / "micro_manipulator").glob("*.FCStd"):
            zipfile.ZipFile(f).extractall(Path(tmp) / f.stem)
        parts = []
        Reader(tmp).walk("Assembly_MicroManipulator", "Assembly", gp_Trsf(), [], parts)
    groups = {}
    for path, s in parts:
        groups.setdefault(group(path), []).append(Shape(s))
    groups["stand"] = [Shape(stl_solid(stand))]
    names = sorted(groups)
    DATA.mkdir(exist_ok=True)
    export_brep(Compound([Compound(groups[n]) for n in names]), str(DATA / "manipulator.brep"))
    (DATA / "manipulator.txt").write_text("\n".join(names) + "\n")
    for n in names:
        b = Compound(groups[n]).bounding_box()
        print(f"{n:24s} {len(groups[n]):3d} shapes  x {b.min.X:6.1f}..{b.max.X:5.1f}  y {b.min.Y:6.1f}..{b.max.Y:5.1f}  z {b.min.Z:6.1f}..{b.max.Z:5.1f}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
