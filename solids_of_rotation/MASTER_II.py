# Try solids of rotation using extrusion along a line: https://blender.stackexchange.com/questions/2866/extrude-along-path
# Other useful topics: 
#   Add keyframe to any data_path (in this case, bevel_end): https://blender.stackexchange.com/questions/34590/how-to-find-the-data-path-for-scripted-keyframes
#   Scripting Curves in blender: https://medium.com/@behreajj/scripting-curves-in-blender-with-python-c487097efd13
#   Change origin of object:
#       - https://blenderartists.org/t/modifying-object-origin-with-python/507305
#       - https://blender.stackexchange.com/questions/70098/how-to-move-an-objects-origin-to-the-center-of-its-bounding-box
#       - https://docs.blender.org/api/blender_python_api_2_70_5/bpy.ops.object.html
#   Cycles Nodes: 
#       - https://blender.stackexchange.com/questions/23436/control-cycles-material-nodes-and-material-properties-in-python
#       - https://blender.stackexchange.com/questions/8475/python-set-material-to-material-slot


import bpy, bmesh
from math import *
from mathutils import Vector
import mathutils, math
import pdb
from mathutils import Vector
import colorsys

def printt(object):
    print('\n'.join(dir(object)))
    
# Move cursor to origin: Shift+C
# Center camera to cursor: Alt+Home

######################################
### Store plot as series of points ###
######################################
# sample data
#coords = [(1,1,0), (-1,1,0), (-1,-1,0), (1, -1, 0)]
#NUMVERTS = 5
#Dphi = 2*pi/NUMVERTS
# calculate x,y coordinate pairs
def fun(x):
    return (x-8)**2/9+1

PLOT_THICKNESS = 0.01
LBOUND = 2
RBOUND = 6
INCR = 0.1
NUMVERTS = int(round((RBOUND-LBOUND)/INCR))+1
plot = [(LBOUND+i*INCR,fun(LBOUND+i*INCR),0) for i in range(NUMVERTS)]

##########################
##########################
##### Plot function ######
##########################
##########################

#######################################################################
### From bezier_curve_from_coords.py: Add curve that needs rotation ###
#######################################################################

NUMVERTS = 128
Dphi = 2*pi/NUMVERTS
# calculate x,y coordinate pairs
coords = [(PLOT_THICKNESS*cos(i*Dphi),PLOT_THICKNESS*sin(-i*Dphi),0) for i in range(NUMVERTS)]

# create the Curve Datablock
extrude_path_data = bpy.data.curves.new('extrude_path', type='CURVE')
extrude_path_data.dimensions = '3D'
extrude_path_data.resolution_u = 2

# map coords to spline
polyline = extrude_path_data.splines.new('POLY')
polyline.points.add(len(coords))

for i, coord in enumerate(coords):
    x,y,z = coord
    polyline.points[i].co = (x, y, z, 1)

xf,yf,zf = coords[0]
polyline.points[len(coords)].co = (xf, yf, zf, 1)

# create Object
plotOB = bpy.data.objects.new('extrude_path_object', extrude_path_data)

# attach to scene and validate context
scn = bpy.context.scene
scn.objects.link(plotOB)
scn.objects.active = plotOB
plotOB.select = True

bevel_plot = bpy.context.scene.objects["extrude_path_object"]


#######################################################################
### Add plot as a path of extrusion (for drawing of plot animation) ###
#######################################################################

plot_path_data = bpy.data.curves.new('plot_path', type='CURVE')
plot_path_data.dimensions = '3D'
plot_path_data.resolution_u = 2

# map coords to spline 
polyline = plot_path_data.splines.new('POLY')
polyline.points.add(len(plot)-1)
for i, pt in enumerate(plot):
    x,y,z = pt
    polyline.points[i].co = (x, y, z, 1)

# create Object
curveOB = bpy.data.objects.new('plot_path', plot_path_data)

# attach to scene and validate context
scn = bpy.context.scene
scn.objects.link(curveOB)
scn.objects.active = curveOB
curveOB.select = True

ob = bpy.context.scene.objects["plot_path"]
curve = ob.data

# Add color
color = colorsys.hsv_to_rgb(0,0,0)
activeObject = bpy.context.active_object
mat = bpy.data.materials.new(name="MaterialName") #set new material to variable
activeObject.data.materials.append(mat)
bpy.context.object.active_material.diffuse_color = color

#############################################################
### Create bevel object from custom curve to bezier curve ###
#############################################################
#bpy.context.object.data.bevel_object = bpy.data.objects["cross_section"]
curve.bevel_object = bevel_plot
curve.use_fill_caps = True


###############
### Animate ###
###############
bpy.context.scene.frame_current = 1
curve.bevel_factor_end = 0
curve.keyframe_insert("bevel_factor_end", frame=1)

bpy.context.scene.frame_current = 20
curve.bevel_factor_end = 1
curve.keyframe_insert("bevel_factor_end", frame=20)





########################################
########################################
##### Rotate Plane to make a solid #####
########################################
########################################


#######################################################################
### From bezier_curve_from_coords.py: Add curve that needs rotation ###
#######################################################################

# create the Curve Datablock
curveData = bpy.data.curves.new('myCurve', type='CURVE')
curveData.dimensions = '3D'
curveData.resolution_u = 2

# map coords to spline
polyline = curveData.splines.new('POLY')
polyline.points.add(len(plot)+2)

xi,yi,zi = (LBOUND, 0, 0)
polyline.points[0].co = (xi, yi, zi, 1)

for i, coord in enumerate(plot):
    x,y,z = coord
    polyline.points[i+1].co = (x, y, z, 1)

xf,yf,zf = (RBOUND, 0, 0)
polyline.points[len(plot)+1].co = (xf, yf, zf, 1)

polyline.points[len(plot)+2].co = (xi, yi, zi, 1)

# create Object
curveOB = bpy.data.objects.new('cross_section', curveData)

# attach to scene and validate context
scn = bpy.context.scene
scn.objects.link(curveOB)
for obj in bpy.data.objects:
    obj.select = False
scn.objects.active = curveOB
curveOB.select = True

## Set origin of cross section to same radius as extrude_path: https://blenderartists.org/t/modifying-object-origin-with-python/507305
# store the location of current 3d cursor
saved_location = bpy.context.scene.cursor_location  # returns a vector

# give 3dcursor new coordinates
bpy.context.scene.cursor_location = Vector((LBOUND,0.0,0.0))

# set the origin on the current object to the 3dcursor location
bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

# set 3dcursor location back to the stored location
bpy.context.scene.cursor_location = saved_location

bevel = bpy.context.scene.objects["cross_section"]

#############################
### Add path of extrusion ###
#############################
#bpy.ops.curve.primitive_bezier_circle_add()
#ob = bpy.context.scene.objects["BezierCircle"]
#bpy.ops.curve.primitive_bezier_curve_add()
NUMVERTS = 512
Dphi = 2*pi/NUMVERTS
MAJOR_RADIUS = LBOUND
# calculate x,y coordinate pairs
coords = [(LBOUND*cos(i*Dphi),0,LBOUND*sin(-i*Dphi)) for i in range(NUMVERTS)]

# create the Curve Datablock
curveData = bpy.data.curves.new('extrude_path', type='CURVE')
curveData.dimensions = '3D'
curveData.resolution_u = 2

# map coords to spline
polyline = curveData.splines.new('POLY')
polyline.points.add(len(coords)+1)
for i, coord in enumerate(coords):
    x,y,z = coord
    polyline.points[i].co = (x, y, z, 1)
    polyline.points[i].tilt = pi/2

x1,y1,z1 = coords[0]
polyline.points[len(coords)].co = (x1, y1, z1, 1)
polyline.points[len(coords)].tilt = pi/2

x2,y2,z2 = coords[1]
polyline.points[len(coords)+1].co = (x2, y2, z2, 1)
polyline.points[len(coords)+1].tilt = pi/2

# create Object
curveOB = bpy.data.objects.new('extrude_path', curveData)

# attach to scene and validate context
scn = bpy.context.scene
scn.objects.link(curveOB)
scn.objects.active = curveOB
curveOB.select = True

ob = bpy.context.scene.objects["extrude_path"]
curve = ob.data

#############################################################
### Create bevel object from custom curve to bezier curve ###
#############################################################
#bpy.context.object.data.bevel_object = bpy.data.objects["cross_section"]
curve.bevel_object = bevel
curve.use_fill_caps = True

# Add color
color = (1,1,1)
activeObject = bpy.context.active_object
mat = bpy.data.materials.new(name="MaterialName") #set new material to variable
activeObject.data.materials.append(mat)
bpy.context.object.active_material.diffuse_color = color


###############
### Animate ###
###############
bpy.context.scene.frame_current = 31
curve.bevel_factor_end = 0
curve.keyframe_insert("bevel_factor_end", frame=31)

bpy.context.scene.frame_current = 50
curve.bevel_factor_end = 1
curve.keyframe_insert("bevel_factor_end", frame=50)


###############################
###############################
##### Add Lamp and Camera #####
###############################
###############################

bpy.ops.object.lamp_add(type='POINT', location=(0,0,25))
bpy.context.object.data.energy = 15
bpy.ops.object.camera_add(location=(0,3,20), rotation = (0,-0,0))

#scene.render.alpha_mode = 'SKY' # in ['TRANSPARENT', 'SKY']
#bpy.data.node_groups["Shader Nodetree"].nodes["Background"].inputs[0].default_value = (1,1,1,1)

bpy.context.scene.render.use_freestyle = True
#bpy.context.scene.render.line_thickness = 0