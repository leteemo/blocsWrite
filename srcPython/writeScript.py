import bpy
from mathutils import Vector
from math import log10
from mathutils.bvhtree import BVHTree
import json

#only if the cubes are not placed
def spawn(x, y, z):

    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for i in range(x):
        for j in range(y):
            for k in range(z):
                bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(i*2, j*2, k*2), scale=(1, 1, 1))
                print((i, j, k))

class Launch():

    def __init__(self,voxeliseAll, cubeSize, saveAt, mesh, end):

        self.frame = 0
        self.nbFrame = 0
        self.nbBlocs = 0
        self.voxeliseAll = voxeliseAll
        self.cubeSize = cubeSize
        self.saveAt = saveAt
        self.listeFrames = {}
        self.nameOfMesh = mesh
        bpy.context.scene.frame_end = end
        bpy.context.scene.frame_current = 0


    def animate(self):
        bpy.app.handlers.frame_change_post.append(self.frameFunction)
        bpy.ops.screen.animation_play()

    #only between mesh
    def check_Collision(self, name1, name2):

        obj1 = bpy.data.objects[name1]
        obj2 = bpy.data.objects[name2]

        mat1 = obj1.matrix_world
        mat2 = obj2.matrix_world

        vert1 = [mat1 @ v.co for v in obj1.data.vertices]
        poly1 = [p.vertices for p in obj1.data.polygons]

        vert2 = [mat2 @ v.co for v in obj2.data.vertices]
        poly2 = [p.vertices for p in obj2.data.polygons]

        bvh1 = BVHTree.FromPolygons( vert1, poly1 )
        bvh2 = BVHTree.FromPolygons( vert2, poly2 )

        if bvh1.overlap(bvh2):
            self.nbCollision += 1
            #values x, y and z
            self.listePos.append([bpy.data.objects[name1].location[0], bpy.data.objects[name1].location[1], bpy.data.objects[name1].location[2]])


    def voxelisation(self):

        self.liste = []
        self.nbCollision = 0
        self.nbBlocs = 0
        self.liste = []
        self.listePos = []

        for i in range(self.cubeSize):
            for j in range(self.cubeSize):
                for k in range(self.cubeSize):

                    if(self.nbBlocs == 0):
                        name = "Cube"

                    if(self.nbBlocs < (1000) and self.nbBlocs != 0):
                        name = "Cube.000"
                        name = name[:(int(log10(self.nbBlocs))+1)*(-1)]
                        name = name+str(self.nbBlocs)

                    if(self.nbBlocs >= (1000)):
                        name = "Cube."
                        name = name+str(self.nbBlocs)

                    self.liste.append(name)
                    self.nbBlocs += 1


        for i in self.liste:
            self.check_Collision(i, self.nameOfMesh)

        self.listeFrames[str(self.nbFrame*self.voxeliseAll)] = self.listePos
        self.nbFrame += 1

    #x and y are not position values
    def frameFunction(self, x, y):

        if(self.frame%self.voxeliseAll == 0):
            self.voxelisation()

        self.frame += 1

        if(self.frame%self.saveAt==0 and self.frame!=0):
            self.voxelisation()
            with open('dataC.json', 'w') as json_file:
                json.dump(self.listeFrames, json_file)
            self.listeFrames = {}
            self.nbFrame = 0
            self.frame = 0

voxel = Launch(voxeliseAll=2, cubeSize=10, saveAt=40, mesh="Icosphere", end=40)
voxel.animate()
