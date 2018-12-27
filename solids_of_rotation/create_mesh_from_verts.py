# Create object from defined vertices:
# https://blender.stackexchange.com/questions/61879/create-mesh-then-add-vertices-to-it-in-python/61893

import bpy
import bmesh

verts = [(1, 1, 1), (0, 0, 0)]  # 2 verts made with XYZ coords
mesh = bpy.data.meshes.new("mesh")  # add a new mesh
obj = bpy.data.objects.new("MyObject", mesh)  # add a new object using the mesh

scene = bpy.context.scene
scene.objects.link(obj)  # put the object into the scene (link)
scene.objects.active = obj  # set as the active object in the scene
obj.select = True  # select object

mesh = bpy.context.object.data
bm = bmesh.new()

for v in verts:
    bm.verts.new(v)  # add a new vert

# make the bmesh the object's mesh
bm.to_mesh(mesh)  
bm.free()  # always do this when finished