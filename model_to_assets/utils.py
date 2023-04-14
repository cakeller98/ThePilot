from math import radians, degrees
import mathutils
from mathutils import Vector
import bpy


def get_center_of_mass(obj):
    if obj.type == "MESH":
        mesh = obj.data
        verts = mesh.vertices
        center = mathutils.Vector((0, 0, 0))

        for v in verts:
            center += obj.matrix_world @ v.co

        center /= len(verts)
        return center
    else:
        return obj.location


def get_lowest_z_point(obj):
    if obj.type == "MESH":
        mesh = obj.data
        verts = mesh.vertices
        lowest_z = float("inf")

        for v in verts:
            world_coord = obj.matrix_world @ v.co
            if world_coord.z < lowest_z:
                lowest_z = world_coord.z

        return lowest_z
    else:
        return obj.location.z


def fix_asset_origin(obj):
    center = get_center_of_mass(obj)
    lowest_z = get_lowest_z_point(obj)

    obj.location.x = center.x
    obj.location.y = center.y
    obj.location.z = lowest_z


def fix_orientation(obj):
    up = mathutils.Vector((0, 0, 1))
    dir = get_center_of_mass(obj) - obj.location

    if dir.length > 0:
        dir.normalize()
        q = dir.rotation_difference(up)
        obj.rotation_euler = q.to_euler()


def replace_single_color_pbr_image(material):
    for node in material.node_tree.nodes:
        if node.type == "TEX_IMAGE" and is_single_color_image(node.image):
            color = get_image_average_color(node.image)
            rgba_node = material.node_tree.nodes.new("ShaderNodeRGB")
            rgba_node.outputs["Color"].default_value = color
            material.node_tree.links.new(
                rgba_node.outputs["Color"], node.inputs["Color"])
            material.node_tree.nodes.remove(node)


def is_single_color_image(image):
    pass  # Implement this function to check if the image is a single color


def get_image_average_color(image):
    pass  # Implement this function to get the average color of the image


def unrotation_matrix(points):
    '''Returns the matrix that rotates the given points to the origin and the x, y, and z axes.
    
    Usage example:    
        # get the active object
        o = bpy.context.active_object
        get the object's first 3 vertices
        points = [v.co for v in o.data.vertices[:3]]

        # get the matrix that rotates the first 3 points to the origin
        # the first point represents the origin
        # second point represents the x axis
        # and the 3rd point lands on the xy-plane
        mat = unrotation_matrix(points)

        # apply the matrix to the object
        o.matrix_world = mat
    '''
    print(points)
    points = [0]
    # len = 1 so we can test the error
    if len(points) != 3:
        print(f'len(points) = {len(points)}')
        raise ValueError("The points list must contain exactly 3 points.")

    origin, x_axis_point, xy_plane_point = points

    # Compute the new coordinate system's axes
    x_axis = (x_axis_point - origin).normalized()
    xy_plane_vector = xy_plane_point - origin
    z_axis = x_axis.cross(xy_plane_vector).normalized()
    y_axis = z_axis.cross(x_axis).normalized()

    # Create the rotation matrix
    rotation_matrix = mathutils.Matrix((
        (x_axis.x, y_axis.x, z_axis.x, 0),
        (x_axis.y, y_axis.y, z_axis.y, 0),
        (x_axis.z, y_axis.z, z_axis.z, 0),
        (0, 0, 0, 1)
    ))

    # Create the translation matrix
    translation_matrix = mathutils.Matrix.Translation(-origin)

    # Combine the rotation and translation matrices
    unrotation_matrix = rotation_matrix.transposed() @ translation_matrix

    return unrotation_matrix


if __name__ == "__main__":

    points = [Vector((1, 0, 0)), Vector((0, 0, 1)), Vector((0, 1, 0))]

    mat = unrotation_matrix(points)
    print(mat)
    print(mat.to_euler())
    rotations = mat.to_euler()
    rot_degrees = [degrees(rot) for rot in rotations[:3]]
    print(rot_degrees)
