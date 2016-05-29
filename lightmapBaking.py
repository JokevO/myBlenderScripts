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

        #image for texture
        image = bpy.data.images.new("map", width=1024, height=1024)
        image.filepath_raw = bpy.path.abspath("//lightmap.png")
        image.file_format = 'PNG'
        image.save() 

        # Remove default
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

    def giveAllObjectsInSceneMaterial(self, mat):
        # remove all current materials
        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                for i in range(len(obj.material_slots)):
                    bpy.ops.object.material_slot_remove({'object': obj})
            obj.data.materials.append(mat)

    def createSphere(self, context):
        #TODO: implement
        return 0
    
    def createSphereMaterial(self):
        #TODO: implement
        return 0
    
    def bakeLightmap(self):
        #TODO: implement
        return 0

    def invoke(self, context, event):
        #change to cycles render  
        self.saveNewBlendFile()
        self.setCylclesRender()
        # material = self.createObjectMaterial()
        # self.giveAllObjectsInSceneMaterial(material)
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