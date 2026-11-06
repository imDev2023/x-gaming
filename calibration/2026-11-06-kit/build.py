"""Build the Crate_01 kit from briefs.md in the live Blender: Crate_01 and five pieces in its style.

Sent as-is through MCP for Blender's execute_blender_code with safe mode on,
so it imports only bpy, bmesh, math and mathutils, uses no lambdas, and keeps
no state between calls: everything it needs is in this file, and rerunning it
rebuilds every piece in place without leaving .001 duplicates.

The style is calibration 2's Crate_01, approved on issue #3: Wood_A parts stand
5 cm proud of recessed parts darkened to 62% through the Col color attribute,
and Metal_A fittings stand 1 cm proud of the wood, so no two visible faces are
coplanar. Every piece has its origin at bottom center and a footprint on the
0.5 m grid, and all pieces share the two materials.
"""

import bpy, bmesh, math
from mathutils import Euler

SHADE_ATTR = "Col"
# Brightness of recessed and shadowed parts: a hand-baked stand-in for ambient
# occlusion, so details still read in an engine without shadows.
RECESS = 0.62
PROUD = 0.01  # how far metal stands proud of the wood it covers
WOOD, METAL = 0, 1  # material slots, the same on every piece

# The startup file's default cube would collide with the pieces.
cube = bpy.data.objects.get("Cube")
if cube is not None:
    bpy.data.objects.remove(cube, do_unlink=True)
for me in [m for m in bpy.data.meshes if m.users == 0]:
    bpy.data.meshes.remove(me)
for mat in [m for m in bpy.data.materials if m.users == 0 and m.name == "Material"]:
    bpy.data.materials.remove(mat)


def material(name, color, metallic, roughness):
    """PBR material whose base color is multiplied by the SHADE_ATTR color attribute."""
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    # Nodes are found by type, never by name, because names are localized.
    p = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    p.inputs["Metallic"].default_value = metallic
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
    m.diffuse_color = (*color, 1.0)  # viewport solid color only
    # Off by default in Blender, which exports doubleSided: true.
    m.use_backface_culling = True
    return m


wood = material("Wood_A", (0.42, 0.24, 0.11), 0.0, 0.85)
metal = material("Metal_A", (0.16, 0.17, 0.19), 1.0, 0.45)


def start():
    bm = bmesh.new()
    bm.loops.layers.float_color.new(SHADE_ATTR)
    bm.loops.layers.uv.new("UVMap")  # uv.verify() would name it "Float2"
    return bm


def box(bm, size, loc, mi, rot=(0.0, 0.0, 0.0), value=1.0):
    """Add a box of `size` centered at `loc`, on material slot `mi`, shaded at `value`."""
    shade = bm.loops.layers.float_color[SHADE_ATTR]
    verts = bmesh.ops.create_cube(bm, size=1.0)["verts"]
    bmesh.ops.scale(bm, vec=size, verts=verts)
    if any(rot):
        bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=Euler(rot).to_matrix(), verts=verts)
    bmesh.ops.translate(bm, vec=loc, verts=verts)
    for f in {f for v in verts for f in v.link_faces}:
        f.material_index = mi
        for loop in f.loops:
            loop[shade] = (value, value, value, 1.0)


def crate(bm, sx, sy, sz, beam=0.1, cap=0.16, bays=1, braces=True, top_caps=True):
    """Crate_01's construction at any size.

    A recessed body, 12 edge beams standing 5 cm proud of it, one diagonal brace
    per bay on each side face, and metal corner caps 1 cm proud of the beams.
    `bays` splits the two long (X) sides with mid posts, joined by cross beams
    over the top and under the bottom; neighbouring braces are mirrored.
    """
    T, hz = beam, sz / 2
    fx, fy, fz = sx / 2 - PROUD, sy / 2 - PROUD, hz - PROUD  # frame outer faces, inside the caps
    bx, by, bz = fx - 0.05, fy - 0.05, fz - 0.05  # body outer faces, 5 cm behind the frame
    px, py = fx - T / 2, fy - T / 2  # beam centers

    # Inset body, darkened as the recess.
    box(bm, (2 * bx, 2 * by, 2 * bz), (0, 0, hz), WOOD, value=RECESS)

    # 12 edge beams.
    for x in (-1, 1):
        for y in (-1, 1):
            box(bm, (T, T, 2 * fz), (x * px, y * py, hz), WOOD)
    rails_z = (hz - fz + T / 2, hz + fz - T / 2)
    for z in rails_z:
        for y in (-1, 1):
            box(bm, (2 * fx - 2 * T, T, T), (0, y * py, z), WOOD)
        for x in (-1, 1):
            box(bm, (T, 2 * fy - 2 * T, T), (x * px, 0, z), WOOD)

    # Mid posts on the long sides, and the cross beams that join them.
    iw, ih, jw = 2 * fx - 2 * T, 2 * fz - 2 * T, 2 * fy - 2 * T  # inner panel sizes
    bay = (iw - (bays - 1) * T) / bays
    for i in range(1, bays):
        x = -iw / 2 + i * bay + (i - 0.5) * T
        for y in (-1, 1):
            box(bm, (T, T, ih), (x, y * py, hz), WOOD)
        for z in rails_z:
            box(bm, (T, jw, T), (x, 0, z), WOOD)

    # Diagonal braces, between the body and the frame face.
    if braces:
        depth = 0.04
        diag, angle = math.hypot(bay, ih), math.atan2(ih, bay)
        for y in (-1, 1):
            for i in range(bays):
                cx = -iw / 2 + bay / 2 + i * (bay + T)
                s = 1 if i % 2 == 0 else -1
                box(bm, (diag - 0.06, depth, 0.09), (cx, y * (by + depth / 2), hz), WOOD, rot=(0, s * y * angle, 0))
        diag, angle = math.hypot(jw, ih), math.atan2(ih, jw)
        for x in (-1, 1):
            box(bm, (depth, diag - 0.06, 0.09), (x * (bx + depth / 2), 0, hz), WOOD, rot=(x * angle, 0, 0))

    # Metal corner caps, larger than the beams and 1 cm proud of them on every face.
    for x in (-1, 1):
        for y in (-1, 1):
            for z in (cap / 2, sz - cap / 2) if top_caps else (cap / 2,):
                box(bm, (cap, cap, cap), (x * (sx / 2 - cap / 2), y * (sy / 2 - cap / 2), z), METAL)


def pallet(bm):
    """A block pallet: five deck boards on three stringers, nine blocks and three bottom boards.

    Everything under the deck is shaded as recess, so the deck's gaps read from
    above; the four corner blocks are metal and stand 1 cm proud, like Crate_01's caps.
    """
    for i in range(5):  # deck boards along X, 16 cm wide with 5 cm gaps
        box(bm, (1.0, 0.16, 0.03), (0, -0.42 + i * 0.21, 0.135), WOOD)
    for x in (-0.42, 0.0, 0.42):  # stringers along Y, 1 cm inside the deck's edges
        box(bm, (0.14, 0.98, 0.025), (x, 0, 0.1075), WOOD, value=RECESS)
    for x in (-0.42, 0.0, 0.42):
        for y in (-0.42, 0.0, 0.42):
            if x and y:
                box(bm, (0.16, 0.16, 0.07), (x, y, 0.06), METAL)
            else:
                box(bm, (0.14, 0.14, 0.07), (x, y, 0.06), WOOD, value=RECESS)
    for y in (-0.42, 0.0, 0.42):  # bottom boards along X
        box(bm, (0.98, 0.14, 0.025), (0, y, 0.0125), WOOD, value=RECESS)


def plank_stack(bm):
    """Three layers of three planks on bearers and stickers, held by two metal straps.

    Planks alternate in tone so neighbours still read apart face-on, and their
    ends are staggered; every plank touches one end of the 2 m footprint.
    """
    for x in (-0.7, 0.7):  # bearers across Y
        box(bm, (0.12, 0.46, 0.07), (x, 0, 0.035), WOOD, value=RECESS)
    cuts = ((2.0, 0.0), (1.94, -0.03), (1.97, 0.015))  # (length, shift along X)
    tones = (1.0, 0.86, 0.94)
    for layer in range(3):
        z0 = 0.07 + layer * 0.16
        for i in range(3):
            length, shift = cuts[(layer + i) % 3]
            box(bm, (length, 0.15, 0.1), (shift, (i - 1) * 0.165, z0 + 0.05), WOOD, value=tones[(2 * layer + i) % 3])
        if layer < 2:
            for x in (-0.7, 0.0, 0.7):  # stickers between layers
                box(bm, (0.06, 0.46, 0.06), (x, 0, z0 + 0.13), WOOD, value=RECESS)
    for x in (-0.35, 0.35):  # straps over the top and down both sides
        box(bm, (0.05, 0.5, PROUD), (x, 0, 0.5 - PROUD / 2), METAL)
        for y in (-1, 1):
            box(bm, (0.05, PROUD, 0.42), (x, y * (0.25 - PROUD / 2), 0.28), METAL)


def lid_box(bm):
    """A small chest: Crate_01's frame without braces, a dark seam, a framed lid, and metal fittings."""
    crate(bm, 1.0, 0.5, 0.38, beam=0.08, cap=0.13, braces=False, top_caps=False)
    # The body frame's top face is at 0.37; a seam 2 cm behind it marks the lid.
    box(bm, (0.94, 0.44, 0.03), (0, 0, 0.385), WOOD, value=RECESS)
    # Lid, z 0.40 to 0.49: a rim flush with the body frame around a panel 5 cm lower.
    lx, ly, r, zl, hl = 0.49, 0.24, 0.08, 0.40, 0.09
    for y in (-1, 1):
        box(bm, (2 * lx, r, hl), (0, y * (ly - r / 2), zl + hl / 2), WOOD)
    for x in (-1, 1):
        box(bm, (r, 2 * ly - 2 * r, hl), (x * (lx - r / 2), 0, zl + hl / 2), WOOD)
    box(bm, (2 * lx - 2 * r, 2 * ly - 2 * r, hl - 0.05), (0, 0, zl + (hl - 0.05) / 2), WOOD, value=RECESS)
    # Lid caps, 1 cm proud of the rim on every face, the underside too: flush
    # with the lid's underside, they would share its plane (checks.py flagged 12 pairs).
    c = 0.13
    for x in (-1, 1):
        for y in (-1, 1):
            box(bm, (c, c, hl + 2 * PROUD), (x * (0.5 - c / 2), y * (0.25 - c / 2), zl + hl / 2), METAL)
    # A latch on the front and two hinges on the back, across the seam.
    box(bm, (0.08, PROUD, 0.12), (0, -(0.25 - PROUD / 2), 0.4), METAL)
    for x in (-0.28, 0.28):
        box(bm, (0.1, PROUD, 0.1), (x, 0.25 - PROUD / 2, 0.4), METAL)


def finish(name, bm):
    """Box-project UVs, write the mesh and link its object, all named `name`."""
    uv = bm.loops.layers.uv["UVMap"]
    # Box-projected UVs, so a texture can be added later without re-unwrapping.
    for f in bm.faces:
        n = f.normal
        axis = 0
        for i in (1, 2):
            if abs(n[i]) > abs(n[axis]):
                axis = i
        a, b = [i for i in range(3) if i != axis]
        for loop in f.loops:
            loop[uv].uv = (loop.vert.co[a] + 0.5, loop.vert.co[b] + 0.5)
    # Geometry is built in world space around the origin, so the origin is bottom
    # center and there are no object transforms to apply.
    me = bpy.data.meshes.get(name) or bpy.data.meshes.new(name)
    me.materials.clear()  # before to_mesh: clear() resets every face's material index to 0
    me.materials.append(wood)
    me.materials.append(metal)
    bm.to_mesh(me)
    bm.free()
    me.color_attributes.active_color = me.color_attributes[SHADE_ATTR]
    ob = bpy.data.objects.get(name) or bpy.data.objects.new(name, me)
    ob.data = me
    ob.location, ob.rotation_euler, ob.scale = (0, 0, 0), (0, 0, 0), (1, 1, 1)
    if ob.name not in bpy.context.scene.collection.objects:
        bpy.context.scene.collection.objects.link(ob)
    print("built", name, "tris", sum(len(p.vertices) - 2 for p in me.polygons))


bm = start()
crate(bm, 1.0, 1.0, 1.0)
finish("Crate_01", bm)

bm = start()
crate(bm, 1.0, 1.0, 0.5)
finish("CrateHalf_01", bm)

bm = start()
crate(bm, 2.0, 1.0, 1.0, bays=2)
finish("CrateLong_01", bm)

bm = start()
pallet(bm)
finish("Pallet_01", bm)

bm = start()
plank_stack(bm)
finish("PlankStack_01", bm)

bm = start()
lid_box(bm)
finish("LidBox_01", bm)
