import bpy
from . import utilities


class CopySkinning(bpy.types.Operator):
    """ Transfer skinning from the active mesh to other selected meshes"""
    bl_idname = "object.copy_skinning"
    bl_label = "copy_skinning"

    @classmethod
    def poll(cls, context):
        return bpy.context.active_object is not None

    def execute(self, context):
        src = bpy.context.active_object
        dst_objects = [x for x in bpy.context.selected_objects if x != bpy.context.active_object]

        # check objects type
        if src.type != 'MESH':
            print('Error : {0} is not a mesh'.format(src.name))
            return {'CANCELLED'}
        for dst in dst_objects:
            if dst.type != 'MESH':
                print('Error : {0} is not a mesh, pass'.format(dst.name))
                dst_objects.remove(dst)

        mod = utilities.get_armature_modifier(src)
        if mod is not None:
            armature = mod.object
        else:
            print('Warning : {0} has no modifier armature'.format(src.name))
            armature = None
        utilities.copy_skinning(dst_objects, armature)

        return {'FINISHED'}


class TransferMeshesData(bpy.types.Operator):
    """ Transfer Meshes Data from old objects (with '_todel' suffix) to new objects """
    bl_idname = "scene.transfer_meshes_data"
    bl_label = "transfer_meshes_data"

    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def execute(self, context):
        utilities.transfer_meshes_data()
        return {'FINISHED'}


class TransferMeshesDrivers(bpy.types.Operator):
    """ Transfer Meshes Drivers from old objects(with '_todel' suffix) to new objects"""
    bl_idname = "scene.transfer_meshes_drivers"
    bl_label = "transfer_meshes_drivers"

    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def execute(self, context):
        utilities.transfer_meshes_drivers()
        return {'FINISHED'}
