# rig_update_tools
add-on for blender to transfer skinning, meshes data or drivers.

![Rig update tools](https://raw.githubusercontent.com/tnzpv/rig_update_tools/master/images/rig_update_tools.jpeg)

Download it inside your addons folder and enable the add-on in Blender.  
The add-on is in the **Rig** Panel.  

- Use `Copy Skinning` to copy the vertex groups and armature modifier of the active object to the other selected objects. 

The Other two tools are used when updating an entire rig : 
![Scene hierarchy](https://raw.githubusercontent.com/tnzpv/rig_update_tools/master/images/scene_hierarchy.jpeg)
Old meshes are already renamed with the suffix `_todel`
We use this suffix to get the correct mesh for each one of them. 
So you don't have to select anything in scene.
> You can choose another suffix instead, but don't forget to replace it in the script!

- Use `Transfer Meshes Drivers` to transfer drivers of every old mesh to its corresponding new mesh.
- Use `Transfer Meshes Data` to transfer modifiers, groups, vertex_groups, and parenting from every old mesh to its corresponding new mesh.
