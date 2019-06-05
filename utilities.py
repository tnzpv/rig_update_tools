import bpy
import re

def get_armature_modifier(ob):
    mod = None
    if ob.type == 'EMPTY' and ob.children:
        # parse children to find armature
        for child in ob.children:
            if child.type == 'MESH':
                mod = ob.modifiers.get('Armature')
                if mod is not None:
                    break

    elif ob.type == 'MESH':
        mod = ob.modifiers.get('Armature')

    return mod

def copy_skinning(dst_objects, armature):
    """ copy skinning from active to selected objects
    -  transfer meshes vertex groups
    - add armature modifier
    :param dst_objects: list of objects to copy data to
    :param armature: armature to use to deform meshes
    """
    try:
        result = bpy.ops.object.data_transfer(data_type='VGROUP_WEIGHTS', vert_mapping='NEAREST',
                                              use_create=True, use_auto_transform=False,
                                              use_object_transform=True, use_max_distance=False,
                                              ray_radius=0, layers_select_src='ALL',
                                              layers_select_dst='NAME', mix_mode='REPLACE', mix_factor=1)
        if result != {'FINISHED'}:
            print('Error while transferring vertex groups: {0}'.format(str(result)))
            return

        for dst in dst_objects:
            if not dst.vertex_groups:
                print('Error: No vertex groups added to {0}'.format(dst.name))
                continue

            armature_modifier = None
            for mod in dst.modifiers:
                if mod.type == 'ARMATURE':
                    armature_modifier = mod
                    break
            if not armature_modifier:
                armature_modifier = dst.modifiers.new('Armature', 'ARMATURE')
                bpy.context.scene.objects.active = dst
                while dst.modifiers[0].name != 'Armature':
                    bpy.ops.object.modifier_move_up(modifier='Armature')

            if armature:
                armature_modifier.object = armature
            else:
                print('Error: Could not connect armature to {0} modifier'.format(dst.name))

    except BaseException as e:
        print('error {0}'.format(str(e)))
        return


def transfer_objects_parent(relative=False, regex='_todel', fromregex=True, selection=None):
    """
    transfert objects parents
    :param relative: when True, 'BONE RELATIVE' activated
    :param regex: str to find if old and new names are slightly differents. todel by default.
    :param fromregex: when True, transfert parent from regex targeted objet to other.
           Else, from nude object to regexed-object
    :return: FINISHED
    """
    matches = dict()
    if regex == '':
        print("WARNING : NO REGEX GIVEN. CANNOT TARGET OBJECTS")

    if selection is None:
        ref = bpy.context.scene.objects
    else:
        ref = selection
    for rgx_ob in ref:
        if re.search(regex, rgx_ob.name):
            nd_name = rgx_ob.name.replace(regex, '')
            nd_ob = bpy.data.objects[nd_name]
            src_object = None
            dst_object = None

            # dans un sens
            if fromregex is True:
                src_object = rgx_ob
                dst_object = nd_ob
            # dans lautre sens
            if fromregex is False:
                src_object = nd_ob
                dst_object = rgx_ob
            print('from {} to {}'.format(src_object.name, dst_object.name))
            matches[src_object] = dst_object
            # prep scene
            if bpy.context.selected_objects:
                bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects[dst_object.name].select = True
            parent = src_object.parent
            if parent is not None:
                bpy.context.scene.objects.active = bpy.data.objects[parent.name]
                    # parenting mode
                if relative is True:
                    # not bone
                    bpy.data.objects[parent.name].select = True
                    bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
                    # bone
                    if src_object.parent_type == 'BONE':
                        bpy.ops.object.mode_set(mode='POSE')
                        layers_bfr = list()
                        for layer in bpy.data.armatures[parent.name].layers:
                            layers_bfr.append(layer)
                        bpy.data.armatures[parent.name].layers = [True, True, True, True, True, True, True, True, True,
                                                                  True, True, True, True, True, True, True, True, True,
                                                                  True, True, True, True, True, True, True, True, True,
                                                                  True, True, True, True, True]
                        bpy.context.active_object.data.bones.active = bpy.data.armatures[parent.name].bones[src_object.parent_bone]
                        bpy.ops.object.parent_set(type='BONE_RELATIVE')
                        bpy.data.armatures[parent.name].layers = layers_bfr
                        bpy.ops.object.mode_set(mode='OBJECT')
                if relative is False:
                    # not bone
                    dst_object.parent = src_object.parent
                    # bone
                    if src_object.parent_type == 'BONE':
                        dst_object.parent_type = 'BONE'
                        dst_object.parent_bone = src_object.parent_bone
            else:
                print("No previous parent to transfer")
    return matches

def transfer_meshes_data(suffix='todel'):
    """ transfer modifiers, groups, vertex groups, and parents
    from old objects (with todel suffix) found in scene to new objects (object without suffix)"""
    for ob in bpy.context.scene.objects:
        if ob.type != 'MESH':
            continue
        if not ob.name.endswith(suffix):
            continue

        new = bpy.context.scene.objects.get(ob.name.split('_{0}'.format(suffix))[0])
        if not new:
            continue

        todel = ob

        if bpy.context.object.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

            # deselect all
        bpy.ops.object.select_all(action='DESELECT')

        new.select = True
        todel.select = True
        bpy.context.scene.objects.active = todel

        # copy groups
        if todel.users_group:
            for t_grp in todel.users_group:
                if new.users_group:
                    new_groups = [x.name for x in new.users_group]
                    if t_grp.name not in new_groups:
                        bpy.data.groups[t_grp.name].objects.link(new)
                else:
                    bpy.data.groups[t_grp.name].objects.link(new)
        # copy properties
        if hasattr(todel, 'show_transparency'):
            new.show_transparency = todel.show_transparency
        # copy modifiers
        bpy.ops.object.make_links_data(type='MODIFIERS')
        bpy.ops.object.copy_skinning()

        ob.data.update()
        ob.data.update()

    transfer_objects_parent(relative=True, regex='_todel', fromregex=True, selection=None)

def dict_visual_props(obj, hidden_props=None, readonly_props=None):
    """
    store constraint data in a dict
    hidden_props= list of props you still need, even if hidden or readonly
    :param obj: from which you want properties
    :param hidden_props: list of props you still need, even if hidden
    :param readonly_props: list of props you still need, even if readonly
    :return: dict of properties and values
    """
    tgtinfos = dict()
    if not hidden_props:
        # we always need type
        hidden_props = ['type']
    if not readonly_props:
        readonly_props = []
    for prop in dir(obj):
        try:
            if not obj.is_property_hidden(prop) and not obj.is_property_readonly(prop):
                tgtinfos[prop] = getattr(obj, prop, None)
            elif prop in hidden_props or prop in readonly_props:
                tgtinfos[prop] = getattr(obj, prop, None)
            else:
                continue
        except TypeError:
            continue
    return tgtinfos

def get_mesh_drivers(obj):
    """
    :param obj: mesh to analyse
    :return dictionary of {[driver]:(driver_info, sub_object_info, list_of_vars)}

    """
    drivers = dict()
    for dr_tuple in obj.animation_data.drivers.items():
        driverob = dr_tuple[1]
        driver = driverob.driver
        vars = driver.variables
        vars_list = list()
        dr_exp = dict_visual_props(driver)
        for var in vars:
            tgts_list = list()
            tgts = var.targets
            var_info = dict_visual_props(var)
            for tgt in tgts:
                tgt_infos = dict_visual_props(tgt)
                tgts_list.append(tgt_infos)
            var_info['tgts_list'] = tgts_list
            vars_list.append(var_info)
        dr_infos = dict_visual_props(driverob)
        drivers[dr_tuple] = [dr_infos, dr_exp, vars_list]

    return drivers

def apply_meshes_drivers(obj, drivers):
    """
    apply drivers to new mesh
    :param obj: mesh to receive
    :param drivers: dict of drivers
    :return:
    """
    for dr_tuple, infos in drivers.items():
        drivername = dr_tuple[1].data_path
        newdr = obj.driver_add(drivername)
        newvar = newdr.driver.variables.new()
        v_liste = infos[2]
        for prop, val in infos[0].items():
            setattr(newdr, prop, val)
        for prop, val in infos[1].items():
            setattr(newdr.driver, prop, val)
        for varinfos in v_liste:
            var = newdr.driver.variables[v_liste.index(varinfos)]
            for prop, val in varinfos.items():
                if hasattr(var, prop):
                    setattr(var, prop, val)
                elif prop == 'tgts_list':
                    tgt_list = val
                    for tgtdc in tgt_list:
                        target = var.targets[tgt_list.index(tgtdc)]
                        for p, v in tgtdc.items():
                            setattr(target, p, v)

def transfer_meshes_drivers(suffix='_todel'):
    """ transfer all meshes drivers from old objects to delete in scene to the new ones"""
    for ob in bpy.context.scene.objects:
        if ob.type != 'MESH':
            continue
        if not ob.name.endswith(suffix):
            continue

        new = bpy.context.scene.objects.get(ob.name.split('_{0}'.format(suffix))[0])
        if not new:
            continue

        todel = ob
        if bpy.context.object.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        # deselect all
        bpy.ops.object.select_all(action='DESELECT')

        new.select = True
        todel.select = True

        bpy.context.scene.objects.active = todel
        if hasattr(todel.animation_data, "drivers"):
            drs = get_mesh_drivers(todel)
            print('Info : applying drivers: {} on {}'.format(drs, new))
            apply_meshes_drivers(new, drs)
        else:
            continue
    print('FINISHED')