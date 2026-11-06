"""Run the Blender side of WORKFLOW.md's done checks on the dock set and print a JSON report.

Adapted from the crate kit's checks.py (calibration/2026-11-06-kit): the same checks,
once per piece, against each piece's brief in briefs.md. The pieces are placed in the
dock layout for looks, so bounds are measured around each piece's own origin (mesh
coordinates), which is what export.py writes. Sent as-is through execute_blender_code
with safe mode on, which blocks open(), so the report is printed, not written.
"""

import bpy, bmesh, json

# From briefs.md: local bounds (min, max) in metres, triangle budget, materials.
PIECES = {
    "Crane_01": ((-2.2, -1.85, 0.0), (1.9, 1.85, 7.71), 2500, ["Glass_A", "Paint_Yellow", "Steel_A"]),
    "CraneJib_01": ((-0.12, -0.65, -0.56), (12.3, 0.65, 0.56), 1200, ["Paint_Yellow", "Steel_A"]),
    "CraneHook_01": ((-0.2, -0.14, -0.023), (0.2, 0.14, 0.85), 300, ["Paint_Orange", "Steel_A"]),
    "Boat_01": ((-6.2, -2.381, -0.8), (6.5, 2.2, 9.0), 5000,
                ["Glass_A", "Hull_A", "Paint_Red", "Paint_White", "Rubber_A", "Steel_A"]),
    "Quay_01": ((-16.0, -5.01, -2.8), (0.01, 5.01, 3.38), 1200, ["Concrete_A", "Glass_A", "Steel_A"]),
}
# The jib is luffed to 50 degrees in the layout for looks; export.py writes it unrotated.
LAYOUT_ROTATED = {"CraneJib_01"}
UV_LAYERS = ["UVMap"]
COLOR_ATTRS = ["Col"]
TOLERANCE_M = 0.005
SCENE_KEEP = {"Camera", "Light"}
EPS_PLANE = 1e-5
EPS_AREA = 1e-6


def faces_of(bm):
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
    """Same-facing pairs (visible z-fighting) and back-to-back pairs (hidden contact faces)."""
    same, back, pairs = 0, 0, []
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
                    pairs.append([round(c, 3) for c in pi] + [round(c, 3) for c in ni])
                else:
                    back += 1
    return same, back, pairs[:6]


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
        bmesh.ops.translate(bm, vec=(0.05 + proud - s / 2, 0, 0.42), verts=cap)
        bm.normal_update()
        results[label] = coplanar_overlaps(faces_of(bm))[0]
        bm.free()
    return results["flush_cap"] > 0 and results["proud_cap"] == 0, results


def check_piece(name, lo_want, hi_want, max_tris, materials):
    ob = bpy.data.objects[name]
    me = ob.data
    bm = bmesh.new()
    bm.from_mesh(me)  # mesh coordinates: around the piece's own origin
    bm.normal_update()
    same, back, pairs = coplanar_overlaps(faces_of(bm))
    bm.free()

    tris = sum(len(p.vertices) - 2 for p in me.polygons)
    lo = [min(v.co[i] for v in me.vertices) for i in range(3)]
    hi = [max(v.co[i] for v in me.vertices) for i in range(3)]
    faces_per_material = {}
    for p in me.polygons:
        key = me.materials[p.material_index].name
        faces_per_material[key] = faces_per_material.get(key, 0) + 1
    uv_layers = [u.name for u in me.uv_layers]
    color_attrs = [c.name for c in me.color_attributes]
    names = [ob.name, me.name] + [m.name for m in me.materials] + uv_layers + color_attrs
    rotation_ok = name in LAYOUT_ROTATED or tuple(ob.rotation_euler) == (0, 0, 0)

    checks = {
        "bounds": all(abs(a - b) <= TOLERANCE_M for a, b in zip(lo + hi, list(lo_want) + list(hi_want))),
        "tris": tris <= max_tris,
        "transforms": tuple(ob.scale) == (1, 1, 1) and rotation_ok,
        "names_clean": me.name == name and uv_layers == UV_LAYERS and color_attrs == COLOR_ATTRS
        and not any(".0" in n for n in names),
        "materials": sorted(m.name for m in me.materials) == materials,
        "every_material_used": sorted(faces_per_material) == materials,
        "single_sided": all(m.use_backface_culling for m in me.materials),
        "no_coplanar_same_facing": same == 0,
    }
    return {
        "triangles": tris,
        "bounds_min_m": [round(v, 3) for v in lo],
        "bounds_max_m": [round(v, 3) for v in hi],
        "location_m": [round(v, 3) for v in ob.location],
        "faces_per_material": faces_per_material,
        "coplanar_same_facing_pairs": same,
        "coplanar_same_facing_examples": pairs,
        "coplanar_back_to_back_pairs": back,
        "checks": checks,
    }


asset_objects = sorted(o.name for o in bpy.data.objects if o.name not in SCENE_KEEP)
test_ok, test_counts = self_test()
pieces = {name: check_piece(name, *spec) for name, spec in PIECES.items()}
set_checks = {
    "only_set_objects": asset_objects == sorted(PIECES),
    "coplanar_check_self_test": test_ok,
}
report = {"pieces": pieces, "asset_objects": asset_objects, "coplanar_self_test": test_counts, "set_checks": set_checks}
print(json.dumps(report, indent=2))
failed = [k for k, v in set_checks.items() if not v]
failed += [f"{n}.{k}" for n, r in pieces.items() for k, v in r["checks"].items() if not v]
print("FAILED CHECKS:", failed if failed else "none")
