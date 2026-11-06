"""Run the Blender side of WORKFLOW.md's done checks on Crate_01 and print a JSON report.

Sent as-is through execute_blender_code with safe mode on, which blocks open(),
so the report is printed and saved from the tool result instead of written here.
"""

import bpy, bmesh, json
from mathutils import Vector

BRIEF = {
    "name": "Crate_01",
    "size_m": (1.0, 1.0, 1.0),
    "size_tolerance_m": 0.005,
    "max_tris": 500,
    "materials": ["Metal_A", "Wood_A"],
}
SCENE_KEEP = {"Camera", "Light"}  # the startup file's own objects, not part of the asset
EPS_PLANE = 1e-5  # metres: faces closer than this to one plane count as coplanar
EPS_AREA = 1e-6  # square metres: overlaps smaller than 1 mm^2 are edge contact, not overlap


def faces_of(bm):
    """Each face as (unit normal, a point on it, its vertices), in world space."""
    return [(f.normal.copy(), f.verts[0].co.copy(), [v.co.copy() for v in f.verts]) for f in bm.faces]


def clip(subject, clipper):
    """Sutherland-Hodgman: the part of polygon `subject` inside convex CCW polygon `clipper`."""
    out = subject
    for i in range(len(clipper)):
        a, b = clipper[i], clipper[(i + 1) % len(clipper)]
        inp, out = out, []
        if not inp:
            break
        for j in range(len(inp)):
            p, q = inp[j], inp[(j + 1) % len(inp)]
            pin = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0]) >= 0
            qin = (b[0] - a[0]) * (q[1] - a[1]) - (b[1] - a[1]) * (q[0] - a[0]) >= 0
            if pin:
                out.append(p)
            if pin != qin:
                dx, dy = q[0] - p[0], q[1] - p[1]
                ex, ey = b[0] - a[0], b[1] - a[1]
                t = (ex * (p[1] - a[1]) - ey * (p[0] - a[0])) / (ey * dx - ex * dy)
                out.append((p[0] + t * dx, p[1] + t * dy))
    return out


def area(poly):
    return 0.5 * sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1] for i in range(len(poly)))


def ccw(poly):
    return poly if area(poly) >= 0 else poly[::-1]


def coplanar_overlaps(faces):
    """Pairs of faces that lie in one plane and overlap.

    Same-facing pairs are visible z-fighting. Back-to-back pairs are hidden
    contact faces inside the model, harmless with backface culling but wasted triangles.
    """
    same, back = 0, 0
    for i in range(len(faces)):
        ni, pi, vi = faces[i]
        u = ni.orthogonal().normalized()
        w = ni.cross(u)
        for j in range(i + 1, len(faces)):
            nj, pj, vj = faces[j]
            d = ni.dot(nj)
            if abs(d) < 0.9999 or abs(ni.dot(pj - pi)) > EPS_PLANE:
                continue
            a = ccw([((p - pi).dot(u), (p - pi).dot(w)) for p in vi])
            b = ccw([((p - pi).dot(u), (p - pi).dot(w)) for p in vj])
            overlap = clip(a, b)
            if len(overlap) >= 3 and abs(area(overlap)) > EPS_AREA:
                if d > 0:
                    same += 1
                else:
                    back += 1
    return same, back


def self_test():
    """The overlap check must flag calibration 1's first build and pass its fix."""
    results = {}
    for label, proud in (("flush_cap", 0.0), ("proud_cap", 0.01)):
        bm = bmesh.new()
        beam = bmesh.ops.create_cube(bm, size=1.0)["verts"]
        bmesh.ops.scale(bm, vec=(0.1, 0.1, 1.0), verts=beam)
        cap = bmesh.ops.create_cube(bm, size=1.0)["verts"]
        s = 0.16 + 2 * proud
        bmesh.ops.scale(bm, vec=(s, s, s), verts=cap)
        # Beam's +X face at x=0.05; the cap's +X face at 0.05 + proud.
        bmesh.ops.translate(bm, vec=(0.05 + proud - s / 2, 0, 0.42), verts=cap)
        bm.normal_update()
        results[label] = coplanar_overlaps(faces_of(bm))[0]
        bm.free()
    return results["flush_cap"] > 0 and results["proud_cap"] == 0, results


ob = bpy.data.objects[BRIEF["name"]]
me = ob.data
bm = bmesh.new()
bm.from_mesh(me)
bm.transform(ob.matrix_world)
bm.normal_update()
same, back = coplanar_overlaps(faces_of(bm))
bm.free()
test_ok, test_counts = self_test()

tris = sum(len(p.vertices) - 2 for p in me.polygons)
world = [ob.matrix_world @ v.co for v in me.vertices]
lo = Vector((min(p.x for p in world), min(p.y for p in world), min(p.z for p in world)))
hi = Vector((max(p.x for p in world), max(p.y for p in world), max(p.z for p in world)))
dims = hi - lo
faces_per_material = {}
for p in me.polygons:
    key = me.materials[p.material_index].name
    faces_per_material[key] = faces_per_material.get(key, 0) + 1
asset_objects = sorted(o.name for o in bpy.data.objects if o.name not in SCENE_KEEP)
names = asset_objects + [me.name] + [m.name for m in me.materials] + [u.name for u in me.uv_layers] + [c.name for c in me.color_attributes]
tol = BRIEF["size_tolerance_m"]

checks = {
    "size": all(abs(d - w) <= tol for d, w in zip(dims, BRIEF["size_m"])),
    "tris": tris <= BRIEF["max_tris"],
    "origin_bottom_center": abs(lo.z) <= 1e-4 and abs(lo.x + hi.x) <= 1e-4 and abs(lo.y + hi.y) <= 1e-4,
    "transforms_applied": tuple(ob.location) == (0, 0, 0)
    and tuple(ob.rotation_euler) == (0, 0, 0)
    and tuple(ob.scale) == (1, 1, 1),
    "names_clean": asset_objects == [BRIEF["name"]] and me.name == BRIEF["name"] and not any(".0" in n for n in names),
    "materials": sorted(m.name for m in me.materials) == BRIEF["materials"],
    "every_material_used": sorted(faces_per_material) == BRIEF["materials"],
    "single_sided": all(m.use_backface_culling for m in me.materials),
    "no_coplanar_same_facing": same == 0,
    "coplanar_check_self_test": test_ok,
}
report = {
    "object": ob.name,
    "triangles": tris,
    "bounds_min_m": [round(v, 4) for v in lo],
    "bounds_max_m": [round(v, 4) for v in hi],
    "dimensions_m": [round(v, 4) for v in dims],
    "faces_per_material": faces_per_material,
    "uv_layers": [u.name for u in me.uv_layers],
    "color_attributes": [c.name for c in me.color_attributes],
    "coplanar_same_facing_pairs": same,
    "coplanar_back_to_back_pairs": back,
    "coplanar_self_test": test_counts,
    "asset_objects": asset_objects,
    "scene_objects": sorted(o.name for o in bpy.data.objects),
    "checks": checks,
}
print(json.dumps(report, indent=2))
if not all(checks.values()):
    print("FAILED CHECKS:", [k for k, v in checks.items() if not v])
