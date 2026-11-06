"""Build the Dockstack dock set from briefs.md in the live Blender: crane, jib, hook, boat and quay.

Sent as-is through MCP for Blender's execute_blender_code with safe mode on, so it
imports only bpy, bmesh, math and mathutils, uses no lambdas, and keeps no state
between calls. Rerunning it rebuilds every piece in place without .001 duplicates.

Helpers and rules come from the crate kit (calibration/2026-11-06-kit/build.py):
base colors are multiplied by the Col color attribute, so parts behind others are
darkened without textures, and a part that covers another stands proud of it, so
no two visible faces are coplanar. Each piece is built around its own origin, its
pivot in the game, then placed in the dock layout for looks; export.py writes each
piece at its origin.
"""

import bpy, bmesh, math
from mathutils import Euler, Vector

SHADE_ATTR = "Col"
RECESS = 0.62  # brightness of recessed and shadowed parts, as in the kit
PROUD = 0.01

cube = bpy.data.objects.get("Cube")
if cube is not None:
    bpy.data.objects.remove(cube, do_unlink=True)


def lin(c):
    """sRGB 0-255 to linear 0-1."""
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def material(name, srgb, roughness):
    """Non-metallic PBR material whose base color is multiplied by the Col attribute."""
    color = tuple(lin(c) for c in srgb)
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    p = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    p.inputs["Metallic"].default_value = 0.0
    p.inputs["Roughness"].default_value = roughness
    attr = next((n for n in nt.nodes if n.type == "VERTEX_COLOR"), None) or nt.nodes.new("ShaderNodeVertexColor")
    attr.layer_name = SHADE_ATTR
    attr.location = (p.location.x - 500, p.location.y)
    mix = next((n for n in nt.nodes if n.type == "MIX"), None) or nt.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    mix.blend_type = "MULTIPLY"
    mix.location = (p.location.x - 250, p.location.y)
    fac = next(s for s in mix.inputs if s.identifier == "Factor_Float")
    a = next(s for s in mix.inputs if s.identifier == "A_Color")
    b = next(s for s in mix.inputs if s.identifier == "B_Color")
    out = next(s for s in mix.outputs if s.identifier == "Result_Color")
    fac.default_value = 1.0
    b.default_value = (*color, 1.0)
    nt.links.new(attr.outputs["Color"], a)
    nt.links.new(out, p.inputs["Base Color"])
    m.diffuse_color = (*color, 1.0)
    m.use_backface_culling = True
    return m


# The video's measured colors divided by its warm grade (SPEC.md), as sRGB.
MATS = {
    "Steel_A": material("Steel_A", (70, 70, 64), 0.7),
    "Paint_Yellow": material("Paint_Yellow", (190, 150, 60), 0.6),
    "Paint_Orange": material("Paint_Orange", (200, 120, 30), 0.6),
    "Glass_A": material("Glass_A", (40, 45, 50), 0.3),
    "Hull_A": material("Hull_A", (52, 46, 40), 0.8),
    "Paint_White": material("Paint_White", (205, 200, 190), 0.7),
    "Paint_Red": material("Paint_Red", (160, 55, 40), 0.6),
    "Rubber_A": material("Rubber_A", (35, 33, 32), 0.9),
    "Concrete_A": material("Concrete_A", (125, 118, 108), 0.9),
}


def part(names):
    """A bmesh with its own ordered material list; faces are added on a named material.

    A dict, not a class: safe mode rejects class definitions.
    """
    bm = bmesh.new()
    bm.loops.layers.float_color.new(SHADE_ATTR)
    bm.loops.layers.uv.new("UVMap")
    return {"bm": bm, "names": list(names)}


def paint(p, faces, mat, value):
    shade = p["bm"].loops.layers.float_color[SHADE_ATTR]
    mi = p["names"].index(mat)
    for f in faces:
        f.material_index = mi
        for loop in f.loops:
            loop[shade] = (value, value, value, 1.0)


def box(p, size, loc, mat, rot=(0.0, 0.0, 0.0), value=1.0):
    bm = p["bm"]
    verts = bmesh.ops.create_cube(bm, size=1.0)["verts"]
    bmesh.ops.scale(bm, vec=size, verts=verts)
    if any(rot):
        bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=Euler(rot).to_matrix(), verts=verts)
    bmesh.ops.translate(bm, vec=loc, verts=verts)
    paint(p, {f for v in verts for f in v.link_faces}, mat, value)


def span(p, lo, hi, mat, value=1.0):
    """Axis-aligned box from corner `lo` to corner `hi`."""
    size = tuple(h - l for l, h in zip(lo, hi))
    loc = tuple((l + h) / 2 for l, h in zip(lo, hi))
    box(p, size, loc, mat, value=value)


def beam(p, a, b, t, mat, t2=None, value=1.0):
    """A square beam of thickness `t` (and `t2` across) from point a to point b."""
    bm = p["bm"]
    a, b = Vector(a), Vector(b)
    d = b - a
    verts = bmesh.ops.create_cube(bm, size=1.0)["verts"]
    bmesh.ops.scale(bm, vec=(d.length, t, t2 or t), verts=verts)
    bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=d.to_track_quat("X", "Z").to_matrix(), verts=verts)
    bmesh.ops.translate(bm, vec=(a + b) / 2, verts=verts)
    paint(p, {f for v in verts for f in v.link_faces}, mat, value)


def cylinder(p, r, h, loc, mat, axis="Z", segments=8, value=1.0):
    bm = p["bm"]
    verts = bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=segments,
                                  radius1=r, radius2=r, depth=h)["verts"]
    if axis == "Y":
        bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=Euler((math.pi / 2, 0, 0)).to_matrix(), verts=verts)
    bmesh.ops.translate(bm, vec=loc, verts=verts)
    paint(p, {f for v in verts for f in v.link_faces}, mat, value)


def torus(p, R, r, loc, mat, m=8, n=4, value=1.0):
    """A ring facing the camera: its axis along Y."""
    bm = p["bm"]
    grid = []
    for i in range(m):
        a = 2 * math.pi * i / m
        radial = Vector((math.cos(a), 0, math.sin(a)))
        row = []
        for j in range(n):
            b = 2 * math.pi * j / n + math.pi / n
            co = Vector(loc) + radial * (R + r * math.cos(b)) + Vector((0, r * math.sin(b), 0))
            row.append(bm.verts.new(co))
        grid.append(row)
    faces = []
    for i in range(m):
        for j in range(n):
            a, b = grid[i][j], grid[(i + 1) % m][j]
            c, d = grid[(i + 1) % m][(j + 1) % n], grid[i][(j + 1) % n]
            faces.append(bm.faces.new((a, b, c, d)))
    bmesh.ops.recalc_face_normals(bm, faces=faces)
    paint(p, faces, mat, value)


def finish(name, part, location=(0, 0, 0), rotation=(0, 0, 0)):
    """Box-project UVs, write the mesh, link its object and place it in the layout."""
    bm = part["bm"]
    bm.normal_update()
    uv = bm.loops.layers.uv["UVMap"]
    for f in bm.faces:
        n = f.normal
        axis = 0
        for i in (1, 2):
            if abs(n[i]) > abs(n[axis]):
                axis = i
        a, b = [i for i in range(3) if i != axis]
        for loop in f.loops:
            loop[uv].uv = (loop.vert.co[a] + 0.5, loop.vert.co[b] + 0.5)
    me = bpy.data.meshes.get(name) or bpy.data.meshes.new(name)
    me.materials.clear()  # before to_mesh: clear() resets every face's material index to 0
    for mat in part["names"]:
        me.materials.append(MATS[mat])
    bm.to_mesh(me)
    bm.free()
    me.color_attributes.active_color = me.color_attributes[SHADE_ATTR]
    ob = bpy.data.objects.get(name) or bpy.data.objects.new(name, me)
    ob.data = me
    ob.location, ob.rotation_euler, ob.scale = location, rotation, (1, 1, 1)
    if ob.name not in bpy.context.scene.collection.objects:
        bpy.context.scene.collection.objects.link(ob)
    print("built", name, "tris", sum(len(p.vertices) - 2 for p in me.polygons))


# Dock layout, in metres, Blender axes (X right, Y away from the camera, Z up); water at z = 0.
BOAT_AT = (0.0, 0.0, 0.0)
QUAY_AT = (-7.4, 0.0, 1.6)
CRANE_AT = (-10.0, 0.0, 1.6)
HINGE = (1.5, 0.0, 5.4)  # jib heel hinge, from the crane's origin
JIB_LEN = 12.0
LAYOUT_LUFF = math.radians(50)


def crane():
    p = part(["Steel_A", "Paint_Yellow", "Glass_A"])
    # Splayed portal legs on bogies, joined by a top frame.
    for x in (-1, 1):
        for y in (-1, 1):
            beam(p, (1.6 * x, 1.6 * y, 0.2), (1.2 * x, 1.2 * y, 4.42), 0.3, "Steel_A")
            span(p, (1.6 * x - 0.3, 1.6 * y - 0.25, 0.0), (1.6 * x + 0.3, 1.6 * y + 0.25, 0.2), "Steel_A", value=RECESS)
    for y in (-1, 1):
        span(p, (-1.42, 1.2 * y - 0.16, 4.3), (1.42, 1.2 * y + 0.16, 4.6), "Steel_A")
    for x in (-1, 1):
        span(p, (1.2 * x - 0.15, -1.04, 4.31), (1.2 * x + 0.15, 1.04, 4.59), "Steel_A")
    # X bracing on all four sides, between points on the splayed legs; the two
    # diagonals of a cross differ in depth and size, so their faces never share a plane.
    def leg(z):
        return 1.6 - 0.4 * (z - 0.2) / 4.22  # a leg's distance from the centre at height z

    for y in (-1, 1):
        for s, (t, inset) in ((1, (0.12, 0.0)), (-1, (0.1, 0.03))):
            beam(p, (-s * leg(0.6), y * (leg(0.6) - inset), 0.6), (s * leg(4.1), y * (leg(4.1) - inset), 4.1), t, "Steel_A")
    for x in (-1, 1):
        for s, (t, inset) in ((1, (0.12, 0.0)), (-1, (0.1, 0.03))):
            beam(p, (x * (leg(0.6) - inset), -s * leg(0.6), 0.6), (x * (leg(4.1) - inset), s * leg(4.1), 4.1), t,
                 "Steel_A", value=RECESS)
    # Slewing ring, machinery house with its cab, counterweight and roof.
    cylinder(p, 1.25, 0.3, (0, 0, 4.75), "Steel_A", segments=12, value=RECESS)
    span(p, (-1.6, -1.35, 4.9), (1.2, 1.35, 6.9), "Paint_Yellow")
    span(p, (-2.2, -1.1, 5.1), (-1.59, 1.1, 6.4), "Steel_A")
    span(p, (-1.7, -1.45, 6.9), (1.3, 1.45, 7.05), "Steel_A", value=RECESS)
    # Cab windows on the near side and the front, 1 cm proud.
    span(p, (0.1, -1.36, 5.7), (1.0, -1.35, 6.5), "Glass_A")
    span(p, (-0.9, -1.36, 5.7), (-0.2, -1.35, 6.5), "Glass_A")
    span(p, (1.2, -0.9, 5.7), (1.21, 0.9, 6.5), "Glass_A")
    # A-frame on the roof for the luffing ropes, with a sheave at its apex.
    for y in (-0.6, 0.6):
        beam(p, (-1.3, y, 7.0), (-0.5, y, 7.55), 0.14, "Steel_A")
        beam(p, (0.5, y, 7.0), (-0.5, y * 1.02, 7.55), 0.12, "Steel_A")
    cylinder(p, 0.16, 1.4, (-0.5, 0, 7.55), "Paint_Yellow", axis="Y", segments=8)
    # Heel lugs that carry the jib's hinge pin.
    for y in (-0.62, 0.62):
        span(p, (1.19, y - 0.06, 5.1), (1.75, y + 0.06, 5.7), "Steel_A")
    return p


def jib():
    p = part(["Steel_A", "Paint_Yellow"])
    L = JIB_LEN

    def half(x):
        return 0.5 - 0.25 * x / L  # half-width of the tapering truss

    chords = [(y, z) for y in (-1, 1) for z in (-1, 1)]
    for y, z in chords:
        beam(p, (0.0, y * 0.5, z * 0.5), (L, y * 0.25, z * 0.25), 0.12, "Steel_A")
    # Zigzag lacing on the near and far faces, alternating thickness so neighbours
    # that meet at a chord never share a face plane.
    n = 12
    for y in (-1, 1):
        for i in range(n):
            x0, x1 = L * i / n, L * (i + 1) / n
            z0, z1 = (-1, 1) if i % 2 == 0 else (1, -1)
            t = 0.06 if i % 2 == 0 else 0.08
            beam(p, (x0, y * half(x0), z0 * half(x0)), (x1, y * half(x1), z1 * half(x1)), t, "Steel_A")
    # Battens across the top and bottom faces.
    for i in range(1, 6):
        x = L * i / 6
        for z in (-1, 1):
            beam(p, (x, -half(x), z * half(x)), (x, half(x), z * half(x)), 0.07, "Steel_A", value=RECESS)
    cylinder(p, 0.12, 1.3, (0, 0, 0), "Steel_A", axis="Y")  # hinge pin
    # Sheave head at the tip, with the rope point under it at (L, 0, -0.35).
    span(p, (L - 0.25, -0.3, -0.25), (L + 0.3, 0.3, 0.3), "Paint_Yellow")
    cylinder(p, 0.22, 0.2, (L, 0, -0.1), "Steel_A", axis="Y", segments=8, value=RECESS)
    return p


def hook():
    p = part(["Paint_Orange", "Steel_A"])
    span(p, (-0.2, -0.13, 0.35), (0.2, 0.13, 0.8), "Paint_Orange")
    for y in (-1, 1):  # cheek plates, proud of the block
        span(p, (-0.16, y * 0.13 - 0.01 * (y < 0), 0.4), (0.16, y * 0.13 + 0.01 * (y > 0), 0.75), "Paint_Orange", value=0.8)
    span(p, (-0.07, -0.07, 0.8), (0.07, 0.07, 0.85), "Steel_A")  # swivel where the rope leaves
    span(p, (-0.04, -0.04, 0.12), (0.04, 0.04, 0.36), "Steel_A")  # shank
    beam(p, (-0.03, 0, 0.12), (0.06, 0, 0.0), 0.07, "Steel_A")  # bowl
    beam(p, (0.06, 0, 0.0), (0.16, 0, 0.08), 0.06, "Steel_A")
    beam(p, (0.16, 0, 0.07), (0.17, 0, 0.2), 0.05, "Steel_A")  # tip
    return p


def boat():
    p = part(["Hull_A", "Paint_White", "Paint_Red", "Glass_A", "Rubber_A", "Steel_A"])
    bm = p["bm"]
    # Hull stations: (x at the deck, x at the keel, half-beam, keel z, sheer z).
    stations = [
        (-6.2, -5.6, 0.12, -0.4, 1.35),
        (-5.4, -5.4, 1.1, -0.65, 1.0),
        (-4.2, -4.2, 1.9, -0.8, 1.0),
        (-2.8, -2.8, 2.2, -0.8, 1.0),
        (4.6, 4.6, 2.2, -0.8, 1.0),
        (6.0, 6.0, 1.9, -0.45, 1.05),
        (6.5, 6.5, 1.6, -0.05, 1.1),
    ]
    sections = []
    for xt, xk, B, keel, sheer in stations:
        # Deck edge, waterline, bilge, keel, then the far side; x rakes from deck to keel.
        prof = [(-B, sheer, 0.0), (-B, 0.0, 0.4), (-0.75 * B, keel + 0.25, 0.8), (0.0, keel, 1.0),
                (0.75 * B, keel + 0.25, 0.8), (B, 0.0, 0.4), (B, sheer, 0.0)]
        sections.append([bm.verts.new((xt + (xk - xt) * k, y, z)) for y, z, k in prof])
    hull = []
    for s in range(len(sections) - 1):
        a, b = sections[s], sections[s + 1]
        for i in range(6):
            hull.append(bm.faces.new((a[i], b[i], b[i + 1], a[i + 1])))
        hull.append(bm.faces.new((a[0], a[6], b[6], b[0])))  # deck strip
    st = sections[0]
    hull.append(bm.faces.new((st[0], st[1], st[5], st[6])))
    hull.append(bm.faces.new((st[1], st[2], st[4], st[5])))
    hull.append(bm.faces.new((st[2], st[3], st[4])))
    hull.append(bm.faces.new(tuple(reversed(sections[-1]))))
    bmesh.ops.recalc_face_normals(bm, faces=hull)
    paint(p, hull, "Hull_A", 1.0)
    deck = [f for f in hull if f.normal.z > 0.9]
    paint(p, deck, "Hull_A", RECESS)

    # Bulwarks along the deck edge, following the bow's taper. Neighbouring segments
    # overlap where they meet, so each starts at its own depth below the deck and ends
    # at its own height: no two share a top or bottom plane (checks.py found 7 pairs).
    for y in (-1, 1):
        pts = [(-5.4, 1.1), (-4.2, 1.9), (-2.8, 2.2)]
        for i in range(2):
            (x0, b0), (x1, b1) = pts[i], pts[i + 1]
            bottom, top = 0.98 - 0.01 * i, 1.3 + 0.01 * i
            mid = (bottom + top) / 2
            beam(p, (x0, y * (b0 - 0.07), mid), (x1, y * (b1 - 0.07), mid), 0.12, "Hull_A", t2=top - bottom)
        span(p, (-2.8, -2.19 if y < 0 else 2.07, 0.96), (2.35, -2.07 if y < 0 else 2.19, 1.32), "Hull_A")
    # Tyre fenders on the near side, hung from the bulwark.
    for x in (-3.6, -2.1, -0.6, 0.9, 2.4, 3.9):
        torus(p, 0.28, 0.1, (x, -2.31, 0.55), "Rubber_A")
        span(p, (x - 0.02, -2.25, 0.82), (x + 0.02, -2.21, 1.28), "Rubber_A")

    # Lower deckhouse, roof edge, windows, door and life ring.
    span(p, (2.4, -1.9, 1.0), (6.0, 1.9, 3.2), "Paint_White")
    span(p, (2.3, -2.0, 3.2), (6.1, 2.0, 3.4), "Paint_Red")
    for x in (3.3, 4.3):
        span(p, (x - 0.3, -1.91, 2.25), (x + 0.3, -1.9, 2.75), "Glass_A")
    span(p, (2.5, -1.91, 1.05), (2.9, -1.9, 2.75), "Paint_White", value=RECESS)  # door, clear of the window
    torus(p, 0.26, 0.07, (5.35, -1.98, 2.3), "Paint_Red")
    span(p, (2.39, -1.2, 2.25), (2.4, 1.2, 2.75), "Glass_A")  # front windows
    # Upper wheelhouse with windows all round its front half, and its roof.
    span(p, (3.0, -1.5, 3.4), (5.2, 1.5, 4.9), "Paint_White")
    span(p, (2.9, -1.6, 4.9), (5.3, 1.6, 5.1), "Paint_Red")
    for x in (3.4, 4.2):
        span(p, (x - 0.3, -1.51, 4.0), (x + 0.3, -1.5, 4.6), "Glass_A")
    span(p, (2.99, -1.2, 4.0), (3.0, 1.2, 4.6), "Glass_A")
    # Railing on the lower roof, near side.
    for x in (2.45, 3.35, 5.25, 6.05):
        span(p, (x - 0.02, -1.97, 3.4), (x + 0.02, -1.93, 4.18), "Steel_A")
    span(p, (2.4, -1.98, 4.18), (6.1, -1.92, 4.22), "Steel_A")
    # Funnel with a dark top band, 1 cm proud of it on every side.
    span(p, (5.45, -0.35, 3.4), (5.95, 0.35, 5.5), "Paint_Red")
    span(p, (5.44, -0.36, 5.5), (5.96, 0.36, 5.8), "Hull_A")
    # Mast with a yard and two radar domes.
    span(p, (4.31, -0.09, 5.1), (4.49, 0.09, 8.8), "Steel_A")
    span(p, (4.34, -0.8, 7.9), (4.46, 0.8, 8.02), "Steel_A")
    cylinder(p, 0.32, 0.2, (4.4, 0, 8.9), "Paint_White", segments=10)
    span(p, (4.49, -0.05, 7.1), (5.0, 0.05, 7.18), "Steel_A")
    cylinder(p, 0.26, 0.16, (5.0, 0, 7.26), "Paint_White", segments=10)
    return p


def quay():
    p = part(["Concrete_A", "Steel_A", "Glass_A"])
    span(p, (-16.0, -5.0, -2.8), (0.0, 5.0, 0.0), "Concrete_A")
    span(p, (-0.5, -5.01, 0.0), (0.01, 5.01, 0.12), "Concrete_A", value=0.85)  # coping along the edge
    span(p, (-16.0, -5.01, -2.8), (-0.5, -5.0, -1.6), "Concrete_A", value=RECESS)  # waterline stain
    for y in (-3.0, 2.0):  # bollards
        cylinder(p, 0.18, 0.42, (-0.9, y, 0.33), "Steel_A", segments=8)
        cylinder(p, 0.25, 0.08, (-0.9, y, 0.58), "Steel_A", segments=8)
    for x, y in ((-3.0, 2.5), (-13.5, -2.0)):  # street lamps
        span(p, (x - 0.06, y - 0.06, 0.0), (x + 0.06, y + 0.06, 3.3), "Steel_A")
        span(p, (x - 0.05, y - 0.05, 3.3), (x + 0.6, y + 0.05, 3.38), "Steel_A")
        span(p, (x + 0.4, y - 0.12, 3.1), (x + 0.7, y + 0.12, 3.29), "Glass_A")
    return p


finish("Crane_01", crane(), CRANE_AT)
hx, hz = CRANE_AT[0] + HINGE[0], CRANE_AT[2] + HINGE[2]
finish("CraneJib_01", jib(), (hx, 0.0, hz), (0.0, -LAYOUT_LUFF, 0.0))
tip_x = hx + JIB_LEN * math.cos(LAYOUT_LUFF)
finish("CraneHook_01", hook(), (tip_x, 0.0, 5.5))
finish("Boat_01", boat(), BOAT_AT)
finish("Quay_01", quay(), QUAY_AT)
