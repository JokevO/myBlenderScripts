import bpy
from mathutils import Vector, Matrix
import random
from bpy.types import Operator  
from bpy.props import FloatVectorProperty, FloatProperty, IntProperty

class createPolygonOcean(bpy.types.Operator):  
  bl_idname = "object.create_polygon_ocean"  
  bl_label = "create polygon ocean"
  bl_options = {'REGISTER', 'UNDO'}

  gridRadius = FloatProperty(  
    name  = 'Radius grid',  
    default  = 10.0,  
    description = "size of the grid" )  

  xSubdivisions = IntProperty(  
    name  = 'X subdivisions',  
    default  = 10,  
    description = "subdivisions in x" )  

  ySubdivisions = IntProperty(  
    name  = 'Y subdivisions',  
    default  = 10,  
    description = "subdivisions in y" )

  framesForAnimation = IntProperty(  
    name  = 'frames per animation',  
    default  = 50,  
    description = "frames in between 2 animations" )    

  numberAnimations = IntProperty(  
    name  = 'number animations',  
    default  = 3,  
    description = "number of animations that will be mixed" )

  minOffset = FloatProperty(  
    name  = 'min offset',  
    default  = -2.0,  
    description = "the minimum offset the vertices can be displaced" ) 

  maxOffset = FloatProperty(  
    name  = 'max offset',  
    default  = 2.0,  
    description = "the maximum offset the vertices can be displaced" ) 

  def createGrid(self):
    print("creating grid")
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=self.xSubdivisions, y_subdivisions=self.ySubdivisions, radius=self.gridRadius, view_align=False, enter_editmode=False, location=(0,0,0))
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.001)
    bpy.ops.object.mode_set(mode = 'OBJECT')
  
  def moveGridVertices(self):
    print("move grid vertices")
    obj = bpy.context.scene.objects.active
    bpy.ops.object.mode_set(mode = 'OBJECT')

    for vert in obj.data.vertices:
      vert.select = True
      rand = random.uniform(self.minOffset, self.maxOffset)
      vert.co.z = rand

  def createShapeKey(self):
    print("create shape key")
    bpy.ops.object.shape_key_add(from_mix=False)


  def animateTimeline(self):
    print("animate timeline")
    obj = bpy.context.scene.objects.active
    shapekeys = obj.data.shape_keys.key_blocks
    for i in range(0, self.numberAnimations):
      frame = self.framesForAnimation * i

      for y in range(0, len(shapekeys)):
        shapekeys[y].value = 0
        shapekeys[y].keyframe_insert("value",frame=frame)

      shapekeys[i].value = 0.5
      shapekeys[i].keyframe_insert("value",frame=frame)

      if i < len(shapekeys) - 1:
        shapekeys[i+1].value = 0.5
        shapekeys[i+1].keyframe_insert("value",frame=frame)

    #last one to loop back to normal
    for k in range(0, len(shapekeys)):
        shapekeys[k].value = 0
        shapekeys[k].keyframe_insert("value",frame=self.framesForAnimation * self.numberAnimations)
    bpy.context.scene.frame_end = self.framesForAnimation * self.numberAnimations


  def execute(self, context):  
      self.createGrid()
      self.moveGridVertices()
      self.createShapeKey()

      for i in range(0, self.numberAnimations):
        self.createShapeKey()
        self.moveGridVertices()

      self.animateTimeline()

      return {'FINISHED'}  


def register():  
    bpy.utils.register_class(createPolygonOcean)  
 
def unregister():
  bpy.utils.unregister_class(createPolygonOcean)


if __name__ == "__main__":  
    register()  