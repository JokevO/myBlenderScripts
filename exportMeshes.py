import bpy

for obj in bpy.data.objects:
	bpy.ops.object.select_all(action='DESELECT')
	if obj.type == 'MESH':
		obj.select = True
		file_path = bpy.path.abspath("//exports/" + obj.name + ".obj")
		bpy.ops.export_scene.obj(filepath=file_path, use_selection=True, use_materials=False, global_scale=5, use_smooth_groups=True, use_normals=True, use_uvs=True)