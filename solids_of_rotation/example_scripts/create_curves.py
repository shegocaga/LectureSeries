# Create curves using data (A second way): https://blender.stackexchange.com/questions/61266/creating-curves-in-python

import bpy
import math
import pdb
from mathutils import Vector

# print all objects
for obj in bpy.data.objects:
    print(obj.name)
    if("Curve" in obj.name):
        print("found")
        bpy.data.scenes["Scene"].objects.unlink(obj)
        bpy.data.objects.remove(obj)

for cur in bpy.data.curves:
    print(cur.name)
    bpy.data.curves.remove(cur)

# sample data
coords = [(1,0,1), (2,0,0), (3,0,1)]

# create the Curve Datablock
curveData = bpy.data.curves.new('myCurve', type='CURVE')
curveData.dimensions = '3D'
curveData.resolution_u = 2

# map coords to spline
polyline = curveData.splines.new('POLY')
polyline.points.add(len(coords))
for i, coord in enumerate(coords):
    x,y,z = coord
    polyline.points[i].co = (x, y, z, 1)
xi,yi,zi = coords[0]
polyline.points[len(coords)].co = (xi, yi, zi, 1)

# create Object
curveOB = bpy.data.objects.new('myCurve', curveData)
curveData.bevel_depth = 0.01

# attach to scene and validate context
scn = bpy.context.scene
scn.objects.link(curveOB)
scn.objects.active = curveOB