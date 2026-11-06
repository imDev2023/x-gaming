"""Export each dock piece alone as a +Y-up GLB into blender/out/, at its own origin.

These are the source models; game/build.sh compresses them into the game's assets.

Sent through execute_blender_code with {checkout} replaced by the absolute path of the
local checkout: the live Blender's working directory is not the repo, and safe mode
blocks os, so the script cannot find the path itself. The pieces stand in the dock
layout for looks, so each is moved to the origin and unrotated for its export, then
put back.
"""

import bpy

OUT_DIR = "{checkout}/calibration/2026-11-06-video2game/blender/out"
FILES = {
    "Crane_01": "crane_01.glb",
    "CraneJib_01": "crane_jib_01.glb",
    "CraneHook_01": "crane_hook_01.glb",
    "Boat_01": "boat_01.glb",
    "Quay_01": "quay_01.glb",
}

for name, file in FILES.items():
    ob = bpy.data.objects[name]
    ob.hide_set(False)
    placed = (tuple(ob.location), tuple(ob.rotation_euler))
    ob.location, ob.rotation_euler = (0, 0, 0), (0, 0, 0)
    for o in bpy.context.view_layer.objects:
        o.select_set(False)
    ob.select_set(True)
    bpy.context.view_layer.objects.active = ob
    out = OUT_DIR + "/" + file
    result = bpy.ops.export_scene.gltf(
        filepath=out,
        export_format="GLB",
        use_selection=True,
        export_yup=True,
        export_apply=True,
        export_vertex_color="MATERIAL",  # the default: export Col because the materials use it
    )
    ob.location, ob.rotation_euler = placed
    print("export", name, result, out)
