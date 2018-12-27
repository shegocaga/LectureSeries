import bpy, bmesh
from math import *
from mathutils import Vector






NUMVERTS = 1000
Dphi = 2*pi/NUMVERTS
# calculate x,y coordinate pairs
coords = [(cos(i*Dphi),sin(i*Dphi),0) for i in range(NUMVERTS)]

bm = bmesh.new()
for v in coords:
    bm.verts.new(v)

# think of this new vertices as bottom of the extruded shape
bottom = bm.faces.new(bm.verts)



# next we create top via extrude operator, note it doesn't move the new face
# we make our 1 face into a list so it can be accepted to geom
top = bmesh.ops.extrude_face_region(bm, geom=[bottom])

# here we move all vertices returned by the previous extrusion
# filter the "geom" list for vertices using list constructor
bmesh.ops.translate(bm, vec=Vector((0,0,1)), verts=[v for v in top["geom"] if isinstance(v,bmesh.types.BMVert)])

bm.normal_update()

me = bpy.data.meshes.new("circle")
bm.to_mesh(me)
# add bmesh to scene
ob = bpy.data.objects.new("circle",me)
bpy.context.scene.objects.link(ob)
bpy.context.scene.update()