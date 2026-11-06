"""Show one kit piece alone in the live Blender, for the bridge's look tool.

Every piece sits at the origin, so the others are hidden in the view layer
while one is looked at. Set SHOW to a piece's name, or to "" to show them all.
Sent through execute_blender_code; GUI only, since a headless rebuild never looks.
"""

import bpy

SHOW = "Crate_01"
PIECES = ("Crate_01", "CrateHalf_01", "CrateLong_01", "Pallet_01", "PlankStack_01", "LidBox_01")

for name in PIECES:
    ob = bpy.data.objects.get(name)
    if ob is not None:
        ob.hide_set(bool(SHOW) and name != SHOW)
print("showing", SHOW or "all", [o.name for o in bpy.context.view_layer.objects if o.visible_get()])
