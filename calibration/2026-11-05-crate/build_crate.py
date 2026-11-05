"""Build Crate_01 from brief.md, check it, render look views and export a GLB.

Run headless from this folder's parent repo:
  /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup \
    --python calibration/2026-11-05-crate/build_crate.py -- calibration/2026-11-05-crate
"""

import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

OUT = Path(sys.argv[sys.argv.index("--") + 1]).resolve()
LOOK = OUT / "look"
LOOK.mkdir(parents=True, exist_ok=True)

BRIEF = {
    "name": "Crate_01",
    "size_m": (1.0, 1.0, 1.0),
    "size_tolerance_m": 0.005,
    "max_tris": 500,
    "materials": {"Wood_A", "Metal_A"},
}

# Report the starting scene, as the brief asks.
print("SCENE BEFORE:", [(o.name, o.type) for o in bpy.data.objects])
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)


def material(name, color, metallic, roughness):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    p = m.node_tree.nodes["Principled BSDF"]
    p.inputs["Base Color"].default_value = (*color, 1.0)
    p.inputs["Metallic"].default_value = metallic
    p.inputs["Roughness"].default_value = roughness
    m.diffuse_color = (*color, 1.0)  # used by the Workbench look renders
    # Blender leaves backface culling off, which exports as doubleSided: true and
    # makes the engine draw the inside of a closed mesh too.
    m.use_backface_culling = True
    return m


WOOD = material("Wood_A", (0.42, 0.24, 0.11), 0.0, 0.85)
METAL = material("Metal_A", (0.16, 0.17, 0.19), 1.0, 0.45)

parts = []


def box(name, size, loc, mat, rot=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc, rotation=rot)
    o = bpy.context.active_object
    o.name = name
    o.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(mat)
    parts.append(o)
    return o


S = 1.0  # outer size, set by the metal corner caps
H = S / 2
T = 0.1  # frame beam thickness
F = H - 0.01  # outer face of the frame, 1 cm inside the caps so no faces are coplanar
B = F - 0.05  # outer face of the body, 5 cm behind the frame so it reads at 4 m

# Inset body.
box("body", (2 * B, 2 * B, S - 2 * (H - B)), (0, 0, H), WOOD)

# 12 edge beams, standing proud of the body.
for x in (-1, 1):
    for y in (-1, 1):
        box("post", (T, T, 2 * F), (x * (F - T / 2), y * (F - T / 2), H), WOOD)
for z in (H - F + T / 2, H + F - T / 2):
    for y in (-1, 1):
        box("rail_x", (2 * F - 2 * T, T, T), (0, y * (F - T / 2), z), WOOD)
    for x in (-1, 1):
        box("rail_y", (T, 2 * F - 2 * T, T), (x * (F - T / 2), 0, z), WOOD)

# One diagonal brace on each side face, between the body and the frame face.
inner = 2 * F - 2 * T
diag = math.hypot(inner, inner)
angle = math.atan2(inner, inner)
depth = 0.04
mid = B + depth / 2
for y in (-1, 1):
    box("brace_x", (diag - 0.06, depth, 0.09), (0, y * mid, H), WOOD, rot=(0, y * angle, 0))
for x in (-1, 1):
    box("brace_y", (depth, diag - 0.06, 0.09), (x * mid, 0, H), WOOD, rot=(x * angle, 0, 0))

# 8 metal corner caps, larger than the beams and 1 cm proud of them on every face.
C = 0.16
for x in (-1, 1):
    for y in (-1, 1):
        for z in (C / 2, S - C / 2):
            box("cap", (C, C, C), (x * (H - C / 2), y * (H - C / 2), z), METAL)

# Join into one object with clean names and an origin at bottom center.
bpy.ops.object.select_all(action="DESELECT")
for o in parts:
    o.select_set(True)
bpy.context.view_layer.objects.active = parts[0]
bpy.ops.object.join()
crate = bpy.context.active_object
crate.name = BRIEF["name"]
crate.data.name = BRIEF["name"]
bpy.context.scene.cursor.location = (0, 0, 0)
bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# Box-project UVs so a texture can be added later without re-unwrapping.
bpy.ops.object.mode_set(mode="EDIT")
bpy.ops.mesh.select_all(action="SELECT")
bpy.ops.uv.cube_project(cube_size=1.0)
bpy.ops.object.mode_set(mode="OBJECT")

# ---- Checks against the brief ----
mesh = crate.data
tris = sum(len(p.vertices) - 2 for p in mesh.polygons)
xs, ys, zs = zip(*(crate.matrix_world @ v.co for v in mesh.vertices))
bounds_min = (min(xs), min(ys), min(zs))
bounds_max = (max(xs), max(ys), max(zs))
dims = tuple(b - a for a, b in zip(bounds_min, bounds_max))
names = sorted(o.name for o in bpy.data.objects)
mats = {m.name for m in mesh.materials}
tol = BRIEF["size_tolerance_m"]
checks = {
    "size": all(abs(d - w) <= tol for d, w in zip(dims, BRIEF["size_m"])),
    "tris": tris <= BRIEF["max_tris"],
    "origin_bottom_center": abs(bounds_min[2]) <= 1e-4
    and abs(bounds_min[0] + bounds_max[0]) <= 1e-4
    and abs(bounds_min[1] + bounds_max[1]) <= 1e-4,
    "transforms_applied": tuple(crate.location) == (0, 0, 0)
    and tuple(crate.rotation_euler) == (0, 0, 0)
    and tuple(crate.scale) == (1, 1, 1),
    "names_clean": names == [BRIEF["name"]] and "." not in mesh.name,
    "materials": mats == BRIEF["materials"],
    "single_sided": all(m.use_backface_culling for m in mesh.materials),
}
report = {
    "object": crate.name,
    "triangles": tris,
    "bounds_min_m": [round(v, 4) for v in bounds_min],
    "bounds_max_m": [round(v, 4) for v in bounds_max],
    "dimensions_m": [round(v, 4) for v in dims],
    "materials": sorted(mats),
    "scene_objects": names,
    "checks": checks,
}
print("REPORT:", json.dumps(report, indent=2))
(OUT / "blender-report.json").write_text(json.dumps(report, indent=2) + "\n")

# ---- Look: solid and wireframe views from four angles ----
scene = bpy.context.scene
scene.render.engine = "BLENDER_WORKBENCH"
scene.display.shading.light = "STUDIO"
scene.display.shading.color_type = "MATERIAL"
scene.display.shading.show_cavity = True
scene.display.shading.show_object_outline = True
scene.render.resolution_x = 480
scene.render.resolution_y = 480
scene.render.film_transparent = False
scene.world = bpy.data.worlds.new("LookWorld") if scene.world is None else scene.world

cam_data = bpy.data.cameras.new("LookCam")
cam_data.type = "ORTHO"
cam_data.ortho_scale = 2.0
cam = bpy.data.objects.new("LookCam", cam_data)
scene.collection.objects.link(cam)
scene.camera = cam
target = Vector((0, 0, 0.5))

# A 1 m reference cube outline next to the crate would clutter the sheet;
# the ortho scale is fixed at 2 m instead, so the crate should fill half the frame.
views = {
    "front": Vector((0, -6, 0.5)),
    "side": Vector((6, 0, 0.5)),
    "top": Vector((0, 0, 6)),
    "three_quarter": Vector((4.5, -4.5, 3.8)),
}


def aim(obj, at):
    obj.rotation_euler = (at - obj.location).to_track_quat("-Z", "Y").to_euler()


def render_all(suffix):
    for view, pos in views.items():
        cam.location = pos
        if view == "top":
            cam.rotation_euler = (0, 0, 0)
        else:
            aim(cam, target)
        scene.render.filepath = str(LOOK / f"{view}_{suffix}.png")
        bpy.ops.render.render(write_still=True)


render_all("solid")
wire = crate.modifiers.new("LookWire", "WIREFRAME")
wire.thickness = 0.006
wire.use_replace = True
render_all("wire")
crate.modifiers.remove(wire)

# The look camera must not reach the export.
bpy.data.objects.remove(cam, do_unlink=True)

# ---- Export ----
bpy.ops.object.select_all(action="DESELECT")
crate.select_set(True)
bpy.context.view_layer.objects.active = crate
glb = OUT / "crate_01.glb"
bpy.ops.export_scene.gltf(
    filepath=str(glb),
    export_format="GLB",
    use_selection=True,
    export_yup=True,
    export_apply=True,
)
print("EXPORTED:", glb, glb.stat().st_size, "bytes")
if not all(checks.values()):
    print("FAILED CHECKS:", [k for k, v in checks.items() if not v])
    sys.exit(1)
