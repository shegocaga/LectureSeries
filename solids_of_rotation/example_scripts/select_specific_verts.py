# Select certain vertices from active object
# https://blender.stackexchange.com/questions/43127/how-do-i-select-specific-vertices-in-blender-using-python-script

import bpy

bpy.ops.object.mode_set(mode = 'OBJECT')
obj = bpy.context.active_object
bpy.ops.object.mode_set(mode = 'EDIT') 
bpy.ops.mesh.select_mode(type="VERT")
bpy.ops.mesh.select_all(action = 'DESELECT')
bpy.ops.object.mode_set(mode = 'OBJECT')
#obj.data.vertices[0].select = True
#bpy.ops.object.mode_set(mode = 'EDIT') 


##### MY EDITS #######

# run over loop?
#ring = []
#ring.append([obj.data.vertices[i] for i in range(0,8)])

#for i in range(0,8):
#    ring[0][i].select = True
    
#bpy.ops.object.mode_set(mode = 'EDIT') 

###### Select from Group #####
vg_group = 1

for i in vgs[vg_group]:
    obj.data.vertices[i].select = True
bpy.ops.object.mode_set(mode = 'EDIT')
