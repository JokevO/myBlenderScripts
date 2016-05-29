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

    def setMaterial(self):
        #TODO: implement
    
    def invoke(self, context, event):
        exportUV()
        setMaterial()
        return {'FINISHED'}

class JokePluginSetObjectMaterial(bpy.types.Operator):
    bl_idname = "object.joke_set_obj"
    bl_label = "Joke prepare obj material for lightmap"
    bl_options = {"REGISTER","UNDO"}

    def saveNewBlendFile(self):
        # TODO: implement this

    def createObjectMaterial(self):
        print("material")
        # Create a new material
        material = bpy.data.materials.new(name="MaterialObject")
        material.use_nodes = True

        #image for texture
        image = bpy.data.images.new("map", width=1024, height=1024)
        image.filepath_raw = bpy.path.abspath("//map.png")
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
            if ob.type == 'MESH':
                for i in range(len(obj.material_slots)):
                    bpy.ops.object.material_slot_remove({'object': obj})
            obj.data.materials.append(mat)

    def createSphere(self, context):
        #TODO: implement
    
    def createSphereMaterial(self):
        #TODO: implement
    
    def bakeLightmap(self):
        #TODO: implement

    def invoke(self, context, event):
        #change to cycles render  
        material = self.createMaterial(context)
        self.giveAllObjectsInSceneMaterial(material)
        return {'FINISHED'}


def register():
    print("Hello World")
    bpy.utils.register_class(JokePluginNames)
    bpy.utils.register_class(JokePluginSetObjectMaterial)


def unregister():
    print("Goodbye World")
    bpy.utils.unregister_class(JokePluginNames)
    bpy.utils.unregister_class(JokePluginSetObjectMaterial)


# This allows you to run the script directly from blenders text editor
# to test the addon without having to install it.
if __name__ == "__main__":
    register()