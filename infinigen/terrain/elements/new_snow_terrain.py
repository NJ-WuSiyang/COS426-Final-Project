def init_plane(name='ground', size=10, location=(0, 0, 0)):
    bpy.ops.mesh.primitive_plane_add(
        size=size, enter_editmode=False, align='WORLD', location=location)
    plane = bpy.context.selected_objects[0]
    plane.name = name
    plane.select_set(False)

