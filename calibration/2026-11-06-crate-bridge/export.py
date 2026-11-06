"""Export Crate_01 alone as a +Y-up GLB next to this file, then save the .blend.

Sent through execute_blender_code with {checkout} replaced by the absolute path
of the local checkout: the live Blender's working directory is not the repo,
and safe mode blocks os, so the script cannot find the path itself.
Safe mode allows export and save operators. The scene keeps its camera and
light, so this also tests that the export takes the selection only.
"""

import bpy

OUT = "{checkout}/calibration/2026-11-06-crate-bridge/crate_01.glb"

ob = bpy.data.objects["Crate_01"]
for o in bpy.context.view_layer.objects:
    o.select_set(False)
ob.select_set(True)
bpy.context.view_layer.objects.active = ob
result = bpy.ops.export_scene.gltf(
    filepath=OUT,
    export_format="GLB",
    use_selection=True,
    export_yup=True,
    export_apply=True,
    export_vertex_color="MATERIAL",  # the default: export Col because the materials use it
)
print("export", result, OUT)
if bpy.data.filepath:  # a headless rebuild has no .blend to save
    bpy.ops.wm.save_mainfile()
    print("saved", bpy.data.filepath)
