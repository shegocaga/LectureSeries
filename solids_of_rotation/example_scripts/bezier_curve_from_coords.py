# Poly/Bezier Curve from list of coordinates: https://blender.stackexchange.com/questions/6750/poly-bezier-curve-from-a-list-of-coordinates


import bpy

# sample data
coords = [(1,1,0), (-1,1,0), (-1,-1,0), (1, -1, 0)]

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

# create Object
curveOB = bpy.data.objects.new('myCurve2', curveData)

# attach to scene and validate context
scn = bpy.context.scene
scn.objects.link(curveOB)
scn.objects.active = curveOB
curveOB.select = True