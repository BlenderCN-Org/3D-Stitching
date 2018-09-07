import bpy
import numpy as np
import os

def get_points(obj1, obj2):
    # input two objects from blender as obj1 and obj2
    
    # find all the vertices for each of the object
    vertices1 = obj1.data.vertices
    vertices2 = obj2.data.vertices

    verts1 = [obj1.matrix_world * vert1.co for vert1 in vertices1] 
    verts2 = [obj2.matrix_world * vert2.co for vert2 in vertices2]

    plain_verts1 = [vert1.to_tuple() for vert1 in verts1]
    plain_verts2 = [vert2.to_tuple() for vert2 in verts2]

    # save the locations for both objects
    location1 = obj1.location
    location2 = obj2.location

    # calculate the distance for each of the vertices in object1 to the location of object2
    point1 = plain_verts1[0]
    distance = np.cbrt(np.square(abs(point1[0] - location2[0]) + abs(point1[1] - location2[1]) + abs(point1[2] - location2[2])))
    for point in plain_verts1:
        if (np.cbrt(np.square(abs(point1[0] - location2[0]) + abs(point1[1] - location2[1]) + abs(point1[2] - location2[2]))) < distance):
             point1 = point
             distance = np.cbrt(np.square(abs(point1[0] - location2[0]) + abs(point1[1] - location2[1]) + abs(point1[2] - location2[2])))   

    # calculate the distance for each of the vertices in object2 to the location of object1
    point2 = plain_verts2[0]
    distance = np.cbrt(np.square(abs(point2[0] - location1[0]) + abs(point2[1] - location1[1]) + abs(point2[2] - location1[2])))
    for point in plain_verts2:
        if (np.cbrt(np.square(abs(point2[0] - location1[0]) + abs(point2[1] - location1[1]) + abs(point2[2] - location1[2]))) < distance):
             point2 = point
             distance = np.cbrt(np.square(abs(point2[0] - location1[0]) + abs(point2[1] - location1[1]) + abs(point2[2] - location1[2]))) 
    return point1, point2


os.chdir('C:\Program Files\Blender Foundation\Blender')
obj1_loc = 'C:\\Users\\liuz1\\AppData\\Roaming\\SPB_Data\\untitled1.obj'
imported_obj1 = bpy.ops.import_scene.obj(filepath = obj1_loc)
print(bpy.context.selected_objects)
obj1 = bpy.context.selected_objects[0]
    
obj2_loc = 'C:\\Users\\liuz1\\AppData\\Roaming\\SPB_Data\\untitled2.obj'
imported_obj2 = bpy.ops.import_scene.obj(filepath = obj2_loc)
print(bpy.context.selected_objects)
obj2 = bpy.context.selected_objects[0]

point1, point2 = get_points(obj1, obj2)
print(point1)
print(point2)