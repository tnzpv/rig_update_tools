import bpy

class RigUpdateTools(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Rig'
    bl_label = "Rig Update Tools"
    bl_idname = "rig_update_tools"

    @classmethod
    def poll(cls, context):
        return context.scene

    def draw(self, context):
        layout = self.layout.column(align=True)
        layout.operator("object.copy_skinning", text='Copy Skinning')
        layout.operator("scene.transfer_meshes_drivers", text='Transfer Meshes Drivers')
        layout.operator("scene.transfer_meshes_data", text='Transfer Meshes Data')
        layout = layout.row()

