import bpy

class alignClass(bpy.types.Operator):
	bl_idname = "object.align"
	bl_label = "align tool"
	bl_options = {'REGISTER', 'UNDO'}

	obj = bpy.context.active_object
	objname = bpy.props.EnumProperty(items=(("0", "Align X", "ALIGN_X"), ("1", "Align Y", "ALIGN_Y"), ("2", "Align Z", "ALIGN_Z")),  
									name = "Align",  
									description = "choose method of alignment")

	def alignX(self, selectionMode):
		selected_verts = []

		if(selectionMode[0]):
			print("selected vertices")
			#selected_verts = [vert for vert in obj.data.vertices if vert.select] 
			selected_verts_index =  [vert.index for vert in self.obj.data.vertices if vert.select] 
		
		print(len(selected_verts))
		self.alignVerticesX(selected_verts)


	def alignVerticesX(self, vertices): 

		to_vert = None
		
		bpy.ops.object.mode_set(mode = 'OBJECT')
		for vert in self.obj.data.vertices:
			print(vertices[0])
			print(vertices[0].index)
			filtered = [x for x in vertices if x == vert.index]
			if (len(filtered) > 0):
				if (to_vert == None):
					to_vert = vert
				vert.co.x = 10.0
		bpy.ops.object.mode_set(mode = 'EDIT')


	def alignEdge(self):
		print("alignEdge")

	def alignFace(self):
		print("alignFace")


	def execute(self, context):
		# confirm selection
		bpy.ops.object.mode_set(mode = 'OBJECT')
		bpy.ops.object.mode_set(mode = 'EDIT')

		selectionMode = bpy.context.scene.tool_settings.mesh_select_mode
		self.alignX(selectionMode)

		return {'FINISHED'}  


def add_to_menu(self, context) :  
	self.layout.operator("object.align", icon = "PLUGIN")  

def register():  
	bpy.utils.register_class(alignClass)  
	bpy.types.VIEW3D_PT_tools_object.append(add_to_menu)

def unregister():
	bpy.utils.unregister_class(alignClass)
	bpy.types.VIEW3D_PT_tools_object.remove(add_to_menu) 

if __name__ == "__main__":
	register()