
# from .preferences import get_addon_preferences
from bpy_extras.io_utils import ExportHelper, ImportHelper
import os
import json
import bpy
from bpy.props import StringProperty, IntProperty
from . import addon_updater_ops


class ModelToAssetsPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    plugin_project_folder: bpy.props.StringProperty(
        name="Plugin Project Folder",
        description="Must contain 'pack_plugin.py'",
        default=r"C:\Users\christopher\iCloudDrive\Code\CakesToys\Model_to_Assets",
        subtype='DIR_PATH'
    )

    # Include imported updater properties

    # addon updater preferences from `__init__`, be sure to copy all of them

    auto_check_update: bpy.props.BoolProperty(
        name="Auto-check for Update",
        description="If enabled, auto-check for updates using an interval",
        default=False
    )

    updater_interval_months: bpy.props.IntProperty(
        name='Months',
        description="Number of months between checking for updates",
        default=0,
        min=0
    )

    updater_interval_days: bpy.props.IntProperty(
        name='Days',
        description="Number of days between checking for updates",
        default=7,
        min=0)

    updater_interval_hours: bpy.props.IntProperty(
        name='Hours',
        description="Number of hours between checking for updates",
        default=0,
        min=0,
        max=23
    )
    updater_interval_minutes: bpy.props.IntProperty(
        name='Minutes',
        description="Number of minutes between checking for updates",
        default=1,
        min=0,
        max=59
    )

    def draw(self, context):
        # make a layout for the addon preferences

        layout = self.layout

        # the first line of the layout is a group of buttons with a label on the left for import/export of preferences

        layout.label(text="Import/Export Preferences")
        row = layout.row()
        row.operator("model_to_assets.export_settings",
                     text="Export Settings")
        row.operator("model_to_assets.import_settings",
                     text="Import Settings")

        addon_updater_ops.update_settings_ui(self, context)


def get_addon_preferences():
    preferences = bpy.context.preferences
    return preferences.addons[__package__].preferences


class EXPORT_OT_ModelToAssetsSettings(bpy.types.Operator, ExportHelper):
    bl_idname = "model_to_assets.export_settings"
    bl_label = "Export ModelToAssets Settings"
    bl_description = "Export ModelToAssets settings to a JSON file"
    bl_options = {'REGISTER'}

    filename_ext = ".json"

    def execute(self, context):
        addon_prefs = get_addon_preferences()

        settings_data = {
            "plugin_project_folder": addon_prefs.plugin_project_folder,
        }

        with open(self.filepath, 'w') as outfile:
            json.dump(settings_data, outfile, indent=4)

        self.report({'INFO'}, f"Settings exported to {self.filepath}")
        return {'FINISHED'}


class IMPORT_OT_ModelToAssetsSettings(bpy.types.Operator, ImportHelper):
    bl_idname = "model_to_assets.import_settings"
    bl_label = "Import ModelToAssets Settings"
    bl_description = "Import ModelToAssets settings from a JSON file"
    bl_options = {'REGISTER'}

    filename_ext = ".json"

    def execute(self, context):
        if not os.path.exists(self.filepath):
            self.report({'ERROR'}, "File not found")
            return {'CANCELLED'}

        with open(self.filepath, 'r') as infile:
            settings_data = json.load(infile)

        addon_prefs = get_addon_preferences()

        addon_prefs.plugin_project_folder = settings_data["plugin_project_folder"]

        self.report({'INFO'}, f"Settings imported from {self.filepath}")
        return {'FINISHED'}


classes = (
    ModelToAssetsPreferences,
    EXPORT_OT_ModelToAssetsSettings,
    IMPORT_OT_ModelToAssetsSettings,
)

# register the classes

_register, _unregister = bpy.utils.register_classes_factory(classes)


def register():
    _register()
    # register the classes


def unregister():
    _unregister()
    # unregister the classes
