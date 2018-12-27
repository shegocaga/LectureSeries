# Create face using points, extrude face
# Souce: https://blender.stackexchange.com/questions/65359/how-to-create-and-extrude-a-bmesh-face

# Other Resources:
# Assign vertices to vertex group: https://blenderartists.org/t/assign-vertices-to-vertex-group/548485
# Selecting vertex groups: https://blender.stackexchange.com/questions/75223/finding-vertices-in-a-vertex-group-using-blenders-python-api

import bpy, bmesh
from math import *
from mathutils import Vector
import mathutils, math

def printt(object):
    print('\n'.join(dir(object)))

NUMVERTS = 8
Dphi = 2*pi/NUMVERTS
# calculate x,y coordinate pairs
coords = [(cos(i*Dphi),sin(i*Dphi),0) for i in range(NUMVERTS)]

bm = bmesh.new()
for v in coords:
    bm.verts.new(v)

# think of this new vertices as bottom of the extruded shape
#bottom = bm.faces.new(bm.verts)
slices = []
slices.append(bm.faces.new(bm.verts))

# next we create top via extrude operator, note it doesn't move the new face
# we make our 1 face into a list so it can be accepted to geom
top = bmesh.ops.extrude_face_region(bm, geom=[slices[0]]) # single iteration. For multiple, based on: top['geom'][i]
slices.append(top)
for i in range(1,11):
    yuki = bmesh.ops.extrude_face_region(bm, geom=[slices[i]['geom'][-1]])
    slices.append(yuki)
    print(yuki, '\n')
    #bmesh.ops.rotate(bm, verts=[v for v in slices[i]["geom"] if isinstance(v,bmesh.types.BMVert)], cent=(0.0, 2.0, 0.0), matrix=mathutils.Matrix.Rotation(math.radians(30.0*i), 3, 'X'))
    bmesh.ops.rotate(bm, verts=[v for v in yuki['geom'] if isinstance(v,bmesh.types.BMVert)], cent=(0.0, 2.0, 0.0), matrix=mathutils.Matrix.Rotation(math.radians(30.0), 3, 'X'))





#bmesh.ops.rotate(bm, verts=[v for v in top["geom"] if isinstance(v,bmesh.types.BMVert)], cent=(0.0, 2.0, 0.0), matrix=mathutils.Matrix.Rotation(math.radians(30.0), 3, 'X'))
#bmesh.ops.rotate(bm, verts=[v for v in top["geom"] if isinstance(v,bmesh.types.BMVert)], cent=(0.0, 2.0, 0.0), matrix=mathutils.Matrix.Rotation(math.radians(30.0), 3, 'X'))

    

bm.normal_update()

me = bpy.data.meshes.new("circle")
bm.to_mesh(me)
# add bmesh to scene
ob = bpy.data.objects.new("circle",me)
bpy.context.scene.objects.link(ob)
bpy.context.scene.update()