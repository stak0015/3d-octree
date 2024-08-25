from __future__ import annotations
from threedeebeetree import Point
import math

def make_ordering(my_coordinate_list: list[Point]) -> list[Point]:
    """
    This balancing algorithm aims to balance an octree through the following steps:
    1. Given a list of 3d coordinates, find the absolute center point by finding the maximum and minimum boundaries of xyz, then finding the nmidpoint for each axis.
    2. Find a point closest to the absolute center point, based on the Euclidean distance of each point relative to the center point, and append it to a new 'sorted' list.
    3. Divide the rest into 8 parts based on the octant direction of each point relative to the now determined center point.
    4. Continue recursion until the list either reaches a length of 1 (making it the center point automatically), or 0 (no more points in that octant).
    
    Time complexity:
    - Best case: O(NlogN) where N is the length of the list
    - Worst case: O(NlogN)
    """
    return make_ordering_aux(my_coordinate_list, new_list=[])

def make_ordering_aux(my_coordinate_list, new_list):
    """Auxiliary function for make_ordering."""
    if len(my_coordinate_list) == 0:
        return
    elif len(my_coordinate_list) == 1:
        new_list.append(my_coordinate_list[0])
        return
    
    abs_center = find_center(my_coordinate_list)
    center = my_coordinate_list[0]
    for point in my_coordinate_list:
        if euclidean_distance(point, abs_center) < euclidean_distance(center, abs_center):
            center = point

    octants = []
    for i in range(8):
        octants.append([])

    new_list.append(center)
    for point in my_coordinate_list:
        if point != center:
            octants[get_octant(point, center)].append(point)
    
    for octant in octants:
        make_ordering_aux(octant, new_list)
    return new_list

def get_octant(key, other_key):
    """
    Gets the corresponding octant of a point based on its position relative to another point.

    Time complexity:
    - Best case: O(1)
    - Worst case: O(1)
    """
    octant = 7
    if key[0] > other_key[0]:
        octant -= 1
    if key[1] > other_key[1]:
        octant -= 2
    if key[2] > other_key[2]:
        octant -= 4
    return octant

def find_center(my_coordinate_list):
    """
    Find the aboslute center point given a list of 3D coordinates.

    Time complexity:
    - Best case: O(N) where N is the length of the list
    - Worst case: O(N)
    """
    min_x, max_x = my_coordinate_list[0][0], my_coordinate_list[0][0]
    min_y, max_y = my_coordinate_list[0][1], my_coordinate_list[0][1]
    min_z, max_z = my_coordinate_list[0][2], my_coordinate_list[0][2]

    for point in my_coordinate_list:
        if point[0] > max_x:
            max_x = point[0]
        if point[0] < min_x:
            min_x = point[0]
        if point[1] > max_y:
            max_y = point[1]
        if point[1] < min_y:
            min_y = point[1]
        if point[2] > max_z:
            max_z = point[2]
        if point[2] < min_z:
            min_z = point[2]

    x_center = (min_x+max_x)/2
    y_center = (min_y+max_y)/2
    z_center = (min_z+max_z)/2

    return (x_center, y_center, z_center)

def euclidean_distance(point1, point2):
    """Calculates the Euclidean distance between two 3D coordinates."""
    return abs(math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2 + (point1[2] - point2[2])**2))