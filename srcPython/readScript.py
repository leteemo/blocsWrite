import bpy
from mathutils import Vector
from math import log10
from mathutils.bvhtree import BVHTree
from time import sleep
import json

#must be sames values than in writeScript
nbBlocs = 0
cubeSize = 12
frame = 0
voxeliseAll = 2
saveAt = 40
listeTemp = []

with open('dataC.json', 'r') as f:
  data = json.load(f)

#place cubes
def anime(frames):

    global listeTemp
    global nbBlocs

    listeTemp = []
    blocs = data[str(frames)]

    for locations in blocs:
        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(locations[0], locations[1], locations[2]), scale=(1, 1, 1))


    nbBlocs = 1

#execution every frames
def frameFunction(x):
    global frame
    global nbFrame
    global listeFrames

    if(frame%voxeliseAll == 0 and (frame != 0)):
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
        anime(frame)

    frame += 1

    if(frame%saveAt==0):
        frame = 0
        nbFrame = 0

bpy.app.handlers.frame_change_post.append(frameFunction)
bpy.ops.screen.animation_play()
