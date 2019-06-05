"""
  rig_update_tools allows to transfer skinning, meshes data or drivers in the selection
"""

bl_info = {
    "name": "Update Tools",
    "author": "TNZPV",
    "version": (1, 0),
    "blender": (2, 7, 9),
    "location": "3D View > Tool Shelf > Rig",
    "description": "Allows to transfer skinning, meshes data or drivers in scene.",
    "category": "Rig"}

import bpy

from . import ui
from . import operators

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)
