# SALVAGED: Create basis polygon for rotation

import bpy, bmesh
from math import *
from mathutils import Vector
import mathutils, math

def printt(object):
    print('\n'.join(dir(object)))

NUMVERTS = 16
Dphi = 2*pi/NUMVERTS
# calculate x,y coordinate pairs
coords = [(cos(i*Dphi),sin(i*Dphi),0) for i in range(NUMVERTS)]
obj_name = "kimi"
rings = 12

bm = bmesh.new()
for v in coords:
    bm.verts.new(v)

# think of this new vertices as bottom of the extruded shape
#bottom = bm.faces.new(bm.verts)
slices = []
slices.append(bm.faces.new(bm.verts))

vgs = [] #Vertex groups, created by slice
vgs.append([i for i in range(NUMVERTS)])

# next we create top via extrude operator, note it doesn't move the new face
# we make our 1 face into a list so it can be accepted to geom
top = bmesh.ops.extrude_face_region(bm, geom=[slices[0]]) # single iteration. For multiple, based on: top['geom'][i]
slices.append(top)
vs = [v for v in top['geom'] if isinstance(v,bmesh.types.BMVert)]
vs_indices = [vs[i].index for i in range(len(vs))]
vgs.append(vs_indices)

for i in range(1,rings):
    yuki = bmesh.ops.extrude_face_region(bm, geom=[slices[i]['geom'][-1]])
    slices.append(yuki)
    print(yuki, '\n')
    vs = [v for v in yuki['geom'] if isinstance(v,bmesh.types.BMVert)]
    vs_indices = [vs[i].index for i in range(len(vs))]
    vgs.append(vs_indices)
    #vg = bm.vertex_groups.new(name=obj_name+'_'+str(i))
    #vg.add(vs_indices, 1.0, 'ADD')
    #bmesh.ops.rotate(bm, verts=vs, cent=(0.0, 2.0, 0.0), matrix=mathutils.Matrix.Rotation(math.radians(360/rings), 3, 'X'))





#bmesh.ops.rotate(bm, verts=[v for v in top["geom"] if isinstance(v,bmesh.types.BMVert)], cent=(0.0, 2.0, 0.0), matrix=mathutils.Matrix.Rotation(math.radians(30.0), 3, 'X'))
#bmesh.ops.rotate(bm, verts=[v for v in top["geom"] if isinstance(v,bmesh.types.BMVert)], cent=(0.0, 2.0, 0.0), matrix=mathutils.Matrix.Rotation(math.radians(30.0), 3, 'X'))

    

bm.normal_update()

me = bpy.data.meshes.new("circle")
bm.to_mesh(me)

# add bmesh to scene
ob = bpy.data.objects.new("circle",me)

# Designate vertex groups (by slice)
#for i in range(1,rings-2):
#    vg = ob.vertex_groups.new(name=obj_name+'_'+str(i))
#    vg.add(vgs[i], 1.0, 'ADD')


bpy.context.scene.objects.link(ob)
bpy.context.scene.update()