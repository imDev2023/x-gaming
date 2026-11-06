"""Export each kit piece alone as a +Y-up GLB next to this file, then save the .blend.

Sent through execute_blender_code with {checkout} replaced by the absolute path
of the local checkout: the live Blender's working directory is not the repo,
and safe mode blocks os, so the script cannot find the path itself.
Every piece sits at the origin, so each export takes its piece alone by selection,
after unhiding it, since show.py may have hidden it for a look.
"""

import bpy

OUT_DIR = "{checkout}/calibration/2026-11-06-kit"
FILES = {
    "Crate_01": "crate_01.glb",
    "CrateHalf_01": "crate_half_01.glb",
    "CrateLong_01": "crate_long_01.glb",
    "Pallet_01": "pallet_01.glb",
    "PlankStack_01": "plank_stack_01.glb",
    "LidBox_01": "lid_box_01.glb",
}

for name, file in FILES.items():
    ob = bpy.data.objects[name]
    ob.hide_set(False)
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
    print("export", name, result, out)
if bpy.data.filepath:  # a headless rebuild has no .blend to save
    bpy.ops.wm.save_mainfile()
    print("saved", bpy.data.filepath)
