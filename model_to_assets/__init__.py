import bpy
from . import operators, preferences, ui, utils, addon_updater_ops

bl_info = {
    "name": "ModelToAssets",
    "author": "CakeBox",
    "version": (0, 0, 120),
    "blender": (3, 5, 0),
    "location": "View3D > Sidebar > ModelToAssets",
    "description": "Generate assets from materials, meshes, hierarchies, and collections",
    "category": "Object",
}

# according to the docs, this is the best way to reload the addon ? is this true ? is this the best way ?
# https://docs.blender.org/api/current/bpy.app.handlers.html#bpy.app.handlers.load_post

_need_reload = "operators" in locals()

if _need_reload:
    import importlib

    addon_updater_ops = importlib.reload(addon_updater_ops)
    operators = importlib.reload(operators)
    preferences = importlib.reload(preferences)
    ui = importlib.reload(ui)
    utils = importlib.reload(utils)


classes = (
)

# register the classes

_register, _unregister = bpy.utils.register_classes_factory(classes)


def register():

    # updater register first
    addon_updater_ops.register(bl_info)

    _register()
    # register the classes

    operators.register()
    preferences.register()
    ui.register()
    # utils.register()


def unregister():

    # updater unregister first
    addon_updater_ops.unregister()

    _unregister()
    # unregister the classes

    operators.unregister()
    preferences.unregister()
    ui.unregister()
    # utils.unregister()


if __name__ == "__main__":
    register()
