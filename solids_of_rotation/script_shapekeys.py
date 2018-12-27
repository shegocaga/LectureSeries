# Scripting shape Keys
# https://blenderartists.org/t/scripting-shape-keys/531997/3


import bpy, bmesh
from math import *
from mathutils import Vector
import mathutils, math

NUMVERTS = 16

def shapeshift(ob):
    for i in range(NUMVERTS):    
        ob.data.vertices[i].co.z += 0.1
        
def rotate(ob, phi):
    mesh = bmesh.from_edit_mesh(obj.data)
    for i in range(NUMVERTS):
        #ob.data.vertices[i]
        bmesh.ops.rotate(mesh, verts=list(mesh.verts), cent=(0.0, 2.0, 0.0), matrix=mathutils.Matrix.Rotation((phi), 3, 'X'))
    bmesh.update_edit_mesh(obj.data)

bpy.context.scene.frame_set(1)
    
obj=bpy.context.active_object
mesh = obj.data

#bpy.ops.object.mode_set(mode='EDIT')
current_mode = bpy.context.active_object.mode

for i in range(10):
    frm = i*5
    bpy.context.scene.frame_set(frm)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.shape_key_add(from_mix=False)
    bpy.ops.object.mode_set(mode='EDIT')    
    if current_mode == 'OBJECT':
        shapeshift(obj)
        #rotate(obj, 30)
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.object.mode_set(mode='OBJECT')
    if current_mode == 'EDIT':
        rotate(obj, 30)
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.object.mode_set(mode='OBJECT')
    if i != 0:
        obj.data.shape_keys.key_blocks['Key ' + str(i)].value = 0
        obj.data.shape_keys.key_blocks['Key ' + str(i)].keyframe_insert("value",frame=frm)
        frm = (i+1)*5
        obj.data.shape_keys.key_blocks['Key ' + str(i)].value = 1
        obj.data.shape_keys.key_blocks['Key ' + str(i)].keyframe_insert("value",frame=frm)
    
        
#bpy.context.object.active_shape_key_index = 2
#bpy.data.shape_keys["Key.008"].key_blocks["Key 2"].value = 1