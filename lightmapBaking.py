bl_info = {
    "name": "blender scripts",
    "author": "Joke van Oijen",
    "location": "Object Tools",
    "description": "This Addon automates baking of lightmaps",
    "category": "UV"}

import bpy
from bpy.props import IntProperty, FloatProperty

class JokePluginNames(bpy.types.Operator):
    bl_idname = "object.joke_set_names"
    bl_label = "Joke Copy object to data names"
    bl_options = {"REGISTER","UNDO"}

    def invoke(self, context, event):
        for obj in bpy.data.objects:
            obj.data.name = obj.name
        return {'FINISHED'}

class JokePluginPrepareObjectForTexture(bpy.types.Operator):
    bl_idname = "object.joke_prepare_for_texture"
    bl_label = "Joke Prepare object for texture"
    bl_options = {"REGISTER","UNDO"}

    def exportUV(self, context):
        #TODO: test export UV
        # set object in edit mode
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.uv.select_all(action='SELECT')

        # create image
        image = bpy.data.images.new("UV", width=1024, height=1024)

        bpy.ops.uv.export_layout(filepath="/Users/jokevanoijen/Desktop/UV.png", check_existing=True, modified=False, mode='PNG', size=(1024, 1024), opacity=1, tessellated=False)

        # write image
        image.filepath_raw = bpy.path.abspath("//UV.png")
        image.file_format = 'PNG'
        image.save()
        bpy.ops.object.mode_set(mode = 'OBJECT')

    def createMaterial(self):
        # Create a new material
        material = bpy.data.materials.new(name="MaterialTexture")
        material.use_nodes = True

        # Remove default
        material_diffuse_bsdf = material.node_tree.nodes.get('Diffuse BSDF')
        material.node_tree.nodes.remove(material_diffuse_bsdf)
        
        #create rest of material
        material_output = material.node_tree.nodes.get('Material Output')
        material_output.location = 600,400
        emission = material.node_tree.nodes.new('ShaderNodeEmission')
        emission.location = 200,500
        emission.inputs['Strength'].default_value = 1.0
        shader_mix = material.node_tree.nodes.new('ShaderNodeMixRGB' )
        shader_mix.inputs['Fac'].default_value = 1.0
        shader_mix.blend_type = 'MULTIPLY'
        shader_mix.location = 400,400
        texture = material.node_tree.nodes.new('ShaderNodeTexImage')
        texture.location = 0,500
        texture2 = material.node_tree.nodes.new('ShaderNodeTexImage')
        texture2.location = 0,200

        # link nodes
        material.node_tree.links.new(emission.inputs[0], texture.outputs[0])
        material.node_tree.links.new(shader_mix.inputs[1], emission.outputs[0])
        material.node_tree.links.new(shader_mix.inputs[2], texture2.outputs[0])
        material.node_tree.links.new(material_output.inputs[0], shader_mix.outputs[0])
        return material

    def setMaterialSelectedObjects(self, context, mat):
        # remove all current materials
        for obj in bpy.context.selected_objects:
            if obj.type == 'MESH':
                for i in range(len(obj.material_slots)):
                    bpy.ops.object.material_slot_remove({'object': obj})
            obj.data.materials.append(mat)

    
    def invoke(self, context, event):
        # exportUV()
        material = self.createMaterial()
        self.setMaterialSelectedObjects(context, material)
        return {'FINISHED'}

class JokePluginSetObjectMaterial(bpy.types.Operator):
    bl_idname = "object.joke_set_obj"
    bl_label = "Joke prepare obj material for lightmap"
    bl_options = {"REGISTER","UNDO"}

    def saveNewBlendFile(self):
        filepath = bpy.data.filepath
        filepath = filepath.replace(".blend", "-lightmap.blend")
        bpy.ops.wm.save_as_mainfile(filepath=filepath)

    def setCylclesRender(self):
        bpy.context.scene.render.engine = 'CYCLES'

    def createObjectMaterial(self):
        # Create a new material
        material = bpy.data.materials.new(name="MaterialObject")
        material.use_nodes = True

        # image for texture
        image = bpy.data.images.new("map", width=1024, height=1024)
        image.filepath_raw = bpy.path.abspath("//lightmap.png")
        image.file_format = 'PNG'
        image.save() 

        # create nodes
        material_diffuse_bsdf = material.node_tree.nodes.get('Diffuse BSDF')
        material_diffuse_bsdf.location = 200, 300
        material_output = material.node_tree.nodes.get('Material Output')
        material_output.location = 600,400
        emission = material.node_tree.nodes.new('ShaderNodeEmission')
        emission.location = 200,500
        emission.inputs['Strength'].default_value = 1.0
        shader_mix = material.node_tree.nodes.new('ShaderNodeMixShader')
        shader_mix.inputs['Fac'].default_value = 1.0
        shader_mix.location = 400,400
        texture = material.node_tree.nodes.new('ShaderNodeTexImage')
        texture.location = 0,500
        texture.image = image

        # link nodes
        material.node_tree.links.new(emission.inputs[0], texture.outputs[0])
        material.node_tree.links.new(shader_mix.inputs[1], emission.outputs[0])
        material.node_tree.links.new(shader_mix.inputs[2], material_diffuse_bsdf.outputs[0])
        material.node_tree.links.new(material_output.inputs[0], shader_mix.outputs[0])
        return material

    def setObjectsMaterial(self, objects, mat):
        # remove all current materials
        for obj in objects:
            if obj.type == 'MESH':
                for i in range(len(obj.material_slots)):
                    bpy.ops.object.material_slot_remove({'object': obj})
            obj.data.materials.append(mat)

    def addSphere(self, context):
        bpy.ops.mesh.primitive_uv_sphere_add( segments=12, size=800, enter_editmode=False, location=(0, 0, 0))
        material = self.createSphereMaterial()
        bpy.context.object.data.materials.append(material)
    
    def createSphereMaterial(self):
        # Create a new material
        material = bpy.data.materials.new(name="MaterialSphere")
        material.use_nodes = True

        # Remove default
        material_diffuse_bsdf = material.node_tree.nodes.get('Diffuse BSDF')
        material.node_tree.nodes.remove(material_diffuse_bsdf)

        material_output = material.node_tree.nodes.get('Material Output')
        material_output.location = 900,300
        emission = material.node_tree.nodes.new('ShaderNodeEmission')
        emission.location = 700,300
        emission.inputs['Strength'].default_value = 1.0
        seperate_xyz = material.node_tree.nodes.new('ShaderNodeSeparateXYZ')
        seperate_xyz.location = 200,300
        texture_coordinate = material.node_tree.nodes.new('ShaderNodeTexCoord')
        texture_coordinate.location = 0,300
        color_ramp = material.node_tree.nodes.new('ShaderNodeValToRGB')
        color_ramp.location = 400,300
        color_ramp.color_ramp.elements[0].position = 0.373
        color_ramp.color_ramp.elements[0].color = (0, 0, 0, 1)
        color_ramp.color_ramp.elements[1].position = 0.536
        color_ramp.color_ramp.elements[1].color = (0.336, 0.381, 0.5, 1)
        color_ramp.color_ramp.elements.new(0.914)
        color_ramp.color_ramp.elements[2].color = (1, 1, 1, 1)

        # link nodes
        material.node_tree.links.new(seperate_xyz.inputs[0], texture_coordinate.outputs[0])
        material.node_tree.links.new(color_ramp.inputs[0], seperate_xyz.outputs[2])
        material.node_tree.links.new(emission.inputs[0], color_ramp.outputs[0])
        material.node_tree.links.new(material_output.inputs[0], emission.outputs[0])
        return material
    
    def bakeLightmap(self, context, objects):
        # select right objects for baking
        bpy.ops.object.select_all(action='DESELECT')
        for obj in objects:
            if obj.type == 'MESH':
                obj.select = True

        # bake lightmap
        bpy.ops.object.bake(type='COMBINED')
        image = bpy.data.images[len(bpy.data.images)-1]
        image.filepath_raw = bpy.path.abspath("//lightmap.png")
        image.save()

    def invoke(self, context, event):
        objects = bpy.context.selected_objects
        self.saveNewBlendFile()
        self.setCylclesRender()
        material = self.createObjectMaterial()
        self.setObjectsMaterial(objects, material)
        self.addSphere(context)
        # self.bakeLightmap(context, objects)
        return {'FINISHED'}


def register():
    print("Hello World")
    bpy.utils.register_class(JokePluginNames)
    bpy.utils.register_class(JokePluginSetObjectMaterial)
    bpy.utils.register_class(JokePluginPrepareObjectForTexture)


def unregister():
    print("Goodbye World")
    bpy.utils.unregister_class(JokePluginNames)
    bpy.utils.unregister_class(JokePluginSetObjectMaterial)
    bpy.utils.unregister_class(JokePluginPrepareObjectForTexture)


# This allows you to run the script directly from blenders text editor
# to test the addon without having to install it.
if __name__ == "__main__":
    register()