import bpy

class templateClass(bpy.types.Operator):
	bl_idname = "templateClass"
	bl_label = "templateClass"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):  
		return {'FINISHED'}  


def register():  
	bpy.utils.register_class(templateClass)  

def unregister():
	bpy.utils.unregister_class(templateClass)

if __name__ == "__main__":
	register()  