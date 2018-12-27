# Select vertices from vertex group
#https://blender.stackexchange.com/questions/75223/finding-vertices-in-a-vertex-group-using-blenders-python-api

o = bpy.context.object
vg_idx = 0
vs = [ v for v in o.data.vertices if vg_idx in [ vg.group for vg in v.groups ] ]