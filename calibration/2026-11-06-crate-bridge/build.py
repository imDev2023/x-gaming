"""Build Crate_01 from ../2026-11-05-crate/brief.md in the live Blender.

Sent as-is through MCP for Blender's execute_blender_code with safe mode on,
so it imports only bpy, bmesh, math and mathutils, uses no lambdas, and keeps
no state between calls: everything it needs is in this file, and rerunning it
rebuilds Crate_01 in place without leaving .001 duplicates.
"""

import bpy, bmesh, math
from mathutils import Euler

NAME = "Crate_01"
SHADE_ATTR = "Col"
# Brightness of the recessed body panels: a hand-baked stand-in for ambient
# occlusion, so the frame and braces still read in an engine without shadows.
RECESS = 0.62

# The startup file's default cube would collide with the crate.
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

bm = bmesh.new()
shade = bm.loops.layers.float_color.new(SHADE_ATTR)
uv = bm.loops.layers.uv.new("UVMap")  # uv.verify() would name it "Float2"


def box(size, loc, mi, rot=(0.0, 0.0, 0.0), value=1.0):
    verts = bmesh.ops.create_cube(bm, size=1.0)["verts"]
    bmesh.ops.scale(bm, vec=size, verts=verts)
    if any(rot):
        bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=Euler(rot).to_matrix(), verts=verts)
    bmesh.ops.translate(bm, vec=loc, verts=verts)
    for f in {f for v in verts for f in v.link_faces}:
        f.material_index = mi
        for loop in f.loops:
            loop[shade] = (value, value, value, 1.0)


S, H, T = 1.0, 0.5, 0.1  # outer size, half size, frame beam thickness
F = H - 0.01  # frame outer face, 1 cm inside the caps, so no faces are coplanar
B = F - 0.05  # body outer face, 5 cm behind the frame, so it reads at 4 m

# Inset body, darkened as the recess.
box((2 * B, 2 * B, S - 2 * (H - B)), (0, 0, H), 0, value=RECESS)

# 12 edge beams, standing proud of the body.
for x in (-1, 1):
    for y in (-1, 1):
        box((T, T, 2 * F), (x * (F - T / 2), y * (F - T / 2), H), 0)
for z in (H - F + T / 2, H + F - T / 2):
    for y in (-1, 1):
        box((2 * F - 2 * T, T, T), (0, y * (F - T / 2), z), 0)
    for x in (-1, 1):
        box((T, 2 * F - 2 * T, T), (x * (F - T / 2), 0, z), 0)

# One diagonal brace on each side face, between the body and the frame face.
inner = 2 * F - 2 * T
diag, angle, depth = math.hypot(inner, inner), math.atan2(inner, inner), 0.04
mid = B + depth / 2
for y in (-1, 1):
    box((diag - 0.06, depth, 0.09), (0, y * mid, H), 0, rot=(0, y * angle, 0))
for x in (-1, 1):
    box((depth, diag - 0.06, 0.09), (x * mid, 0, H), 0, rot=(x * angle, 0, 0))

# 8 metal corner caps, larger than the beams and 1 cm proud of them on every face.
C = 0.16
for x in (-1, 1):
    for y in (-1, 1):
        for z in (C / 2, S - C / 2):
            box((C, C, C), (x * (H - C / 2), y * (H - C / 2), z), 1)

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
me = bpy.data.meshes.get(NAME) or bpy.data.meshes.new(NAME)
me.materials.clear()  # before to_mesh: clear() resets every face's material index to 0
me.materials.append(wood)
me.materials.append(metal)
bm.to_mesh(me)
bm.free()
me.color_attributes.active_color = me.color_attributes[SHADE_ATTR]
ob = bpy.data.objects.get(NAME) or bpy.data.objects.new(NAME, me)
ob.data = me
ob.location, ob.rotation_euler, ob.scale = (0, 0, 0), (0, 0, 0), (1, 1, 1)
if ob.name not in bpy.context.scene.collection.objects:
    bpy.context.scene.collection.objects.link(ob)
print("built", NAME, "tris", sum(len(p.vertices) - 2 for p in me.polygons))
