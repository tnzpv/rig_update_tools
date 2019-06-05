"""
  rig_update_tools allows to transfer skinning, meshes data or drivers in the selection
    Copyright (C) 2019 TNZPV

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
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