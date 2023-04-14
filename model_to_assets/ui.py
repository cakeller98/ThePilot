import bpy


class ModelToAssetsPanel(bpy.types.Panel):
    bl_label = "Model To Assets"
    bl_idname = "OBJECT_PT_model_to_assets"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "ModelToAssets"

    def draw(self, context):
        layout = self.layout
        # make all the layout.column() visually use inset
        # make the background any layout.row() use a different color

        layout = layout.column()

        layout.label(text="Fix Image Interpolation Mode", icon='IMAGE_DATA')
        # layout.operator("object.fix_image_interpolation_mode", icon='IMAGE_DATA')
        # Make Material Into Assets
        layout.label(text="Materials to Assets NEW TEST")
        layout.operator("object.make_material_into_asset",
                        icon='MATERIAL')

        # Make Mesh Object Into Assets
        layout.label(text="Mesh Objects to Assets")
        layout.operator("object.make_mesh_object_into_asset",
                        icon='OBJECT_DATA')
        layout = layout.column()
        # Make Hierarchy Into Assets
        layout.label(text="Hierarchies Assets")
        layout.operator("object.make_hierarchy_into_asset",
                        icon='EMPTY_ARROWS')

        # Make Collection Into Assets
        layout.label(text="Collections to Assets")
        layout.operator("object.make_collection_into_asset",
                        icon='OUTLINER_COLLECTION')


classes = (
    ModelToAssetsPanel,
)

# register the classes

_register, _unregister = bpy.utils.register_classes_factory(classes)


def register():
    _register()
    # register the classes


def unregister():
    _unregister()
    # unregister the classes
