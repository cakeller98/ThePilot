import os
import subprocess
import sys
import bpy


class MakeMaterialIntoAsset(bpy.types.Operator):
    bl_idname = "object.make_material_into_asset"
    bl_label = "Make Material Into Asset"
    bl_options = {'REGISTER', 'UNDO'}

    # Add operator properties here
    material_suffix: bpy.props.StringProperty(
        name="Material Suffix", default="_mat")
    material_prefix: bpy.props.StringProperty(
        name="Material Prefix", default="KB3D_")
    add_suffix: bpy.props.BoolProperty(name="Add Suffix", default=True)
    add_prefix: bpy.props.BoolProperty(name="Add Prefix", default=True)
    all_materials: bpy.props.BoolProperty(name="All Materials", default=False)

    def execute(self, context):
        # Add functionality here
        if self.all_materials:
            objects_to_process = [
                o for o in bpy.context.scene.objects if type(o.data) == bpy.types.Mesh]
        else:
            objects_to_process = [
                o for o in bpy.context.selected_objects if type(o.data) == bpy.types.Mesh]

        # Your operator's code here
        for obj in objects_to_process:
            # Perform the action on obj
            newname = obj.name
            if self.material_prefix is not None:
                newname = self.material_prefix + newname
            if self.material_suffix is not None:
                newname += self.material_suffix
            obj.name = newname
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    # whenever an option is changed, this redraws the operator panel by calling draw()
    # where is draw called?
    # draw is called by the panel that is defined in the panel class
    def check(self, context):
        # call the draw function to redraw the panel
        bpy.context.area.tag_redraw()

        return True


class MakeMaterialIntoAssetOperatorPanel(bpy.types.Panel):
    bl_label = "Make Material Into Asset"
    bl_idname = "OBJECT_PT_make_material_into_asset"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "ModelToAssets"

    def draw(self, context):

        props = context.scene.model_to_assets

        layout = self.layout
        layout = layout.column()
        layout.operator("object.make_material_into_asset",  icon='MATERIAL')
        layout.prop(self, "all_materials")
        row = layout.row()
        row.prop(self, "material_prefix")
        row.enabled = props.add_prefix

        row = layout.row()
        row.prop(self, "material_suffix")
        row.enabled = props.add_suffix

        layout.prop(self, "add_prefix")
        layout.prop(self, "add_suffix")


class MakeMeshObjectIntoAsset(bpy.types.Operator):
    bl_idname = "object.make_mesh_object_into_asset"
    bl_label = "Make Mesh Object Into Asset"
    bl_options = {'REGISTER', 'UNDO'}

    # Add operator properties here

    def execute(self, context):
        # Add functionality here
        return {'FINISHED'}


class MakeHierarchyIntoAsset(bpy.types.Operator):
    bl_idname = "object.make_hierarchy_into_asset"
    bl_label = "Make Hierarchy Into Asset"
    bl_options = {'REGISTER', 'UNDO'}

    # Add operator properties here

    def execute(self, context):
        # Add functionality here
        return {'FINISHED'}


class MakeCollectionIntoAsset(bpy.types.Operator):
    bl_idname = "object.make_collection_into_asset"
    bl_label = "Make Collection Into Asset"
    bl_options = {'REGISTER', 'UNDO'}

    # Add operator properties here

    def execute(self, context):
        # Add functionality here
        return {'FINISHED'}


# register the classes
classes = (
    MakeMaterialIntoAsset,
    MakeMaterialIntoAssetOperatorPanel,
    MakeMeshObjectIntoAsset,
    MakeHierarchyIntoAsset,
    MakeCollectionIntoAsset,
)

_register, _unregister = bpy.utils.register_classes_factory(classes)


def register():
    _register()
    # register the classes


def unregister():
    _unregister()
    # unregister the classes
