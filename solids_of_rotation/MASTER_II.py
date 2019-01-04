# Try solids of rotation using extrusion along a line: https://blender.stackexchange.com/questions/2866/extrude-along-path
# Other useful topics: 
#   Add keyframe to any data_path (in this case, bevel_end): https://blender.stackexchange.com/questions/34590/how-to-find-the-data-path-for-scripted-keyframes
#   Scripting Curves in blender: https://medium.com/@behreajj/scripting-curves-in-blender-with-python-c487097efd13


import bpy, bmesh
from math import *
from mathutils import Vector
import mathutils, math
import pdb
from mathutils import Vector

def printt(object):
    print('\n'.join(dir(object)))
    
# Move cursor to origin: Shift+C
# Center camera to cursor: Alt+Home

### From bezier_curve_from_coords.py: Add curve that needs rotation ###
# sample data
#coords = [(1,1,0), (-1,1,0), (-1,-1,0), (1, -1, 0)]
#NUMVERTS = 5
#Dphi = 2*pi/NUMVERTS
# calculate x,y coordinate pairs
def fun(x):
    return (x**2)/4+0.75

LBOUND = 1
RBOUND = 4
INCR = 0.1
NUMVERTS = int(round((RBOUND-LBOUND)/INCR))
coords = [(LBOUND+i*INCR,fun(LBOUND+i*INCR),0) for i in range(NUMVERTS)]

# create the Curve Datablock
curveData = bpy.data.curves.new('myCurve', type='CURVE')
curveData.dimensions = '3D'
curveData.resolution_u = 2

# map coords to spline
polyline = curveData.splines.new('POLY')
polyline.points.add(len(coords)+2)

xi,yi,zi = (LBOUND, 0, 0)
polyline.points[0].co = (xi, yi, zi, 1)

for i, coord in enumerate(coords):
    x,y,z = coord
    polyline.points[i+1].co = (x, y, z, 1)

xf,yf,zf = (RBOUND, 0, 0)
polyline.points[len(coords)+1].co = (xf, yf, zf, 1)

polyline.points[len(coords)+2].co = (xi, yi, zi, 1)

# create Object
curveOB = bpy.data.objects.new('myCurve2', curveData)

# attach to scene and validate context
scn = bpy.context.scene
scn.objects.link(curveOB)
scn.objects.active = curveOB
curveOB.select = True

bevel = bpy.context.scene.objects["myCurve2"]

### Add Curve to extrude along ###
#bpy.ops.curve.primitive_bezier_circle_add()
#ob = bpy.context.scene.objects["BezierCircle"]
#bpy.ops.curve.primitive_bezier_curve_add()
NUMVERTS = 128
Dphi = 2*pi/NUMVERTS
MAJOR_RADIUS = LBOUND
# calculate x,y coordinate pairs
coords = [(MAJOR_RADIUS*cos(i*Dphi),0,MAJOR_RADIUS*sin(i*Dphi)) for i in range(NUMVERTS)]

# create the Curve Datablock
curveData = bpy.data.curves.new('extrude_curve', type='CURVE')
curveData.dimensions = '3D'
curveData.resolution_u = 2

# map coords to spline
polyline = curveData.splines.new('POLY')
polyline.points.add(len(coords)+1)
for i, coord in enumerate(coords):
    x,y,z = coord
    polyline.points[i].co = (x, y, z, 1)

x1,y1,z1 = coords[0]
polyline.points[len(coords)].co = (x1, y1, z1, 1)
x2,y2,z2 = coords[1]
polyline.points[len(coords)+1].co = (x2, y2, z2, 1)

# create Object
curveOB = bpy.data.objects.new('extrude_curve', curveData)

# attach to scene and validate context
scn = bpy.context.scene
scn.objects.link(curveOB)
scn.objects.active = curveOB
curveOB.select = True

ob = bpy.context.scene.objects["extrude_curve"]
curve = ob.data


### Create bevel object from custom curve to bezier curve ###
#bpy.context.object.data.bevel_object = bpy.data.objects["myCurve2"]
curve.bevel_object = bevel
curve.use_fill_caps = True



### Animate ###
bpy.context.scene.frame_current = 1
curve.bevel_factor_end = 0
curve.keyframe_insert("bevel_factor_end", frame=1)

bpy.context.scene.frame_current = 20
curve.bevel_factor_end = 1
curve.keyframe_insert("bevel_factor_end", frame=20)
