# # #a star tutorial
import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
import thorpy as th
from scipy.spatial import distance


class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

def a_star(maze,start,end):
    # for row in maze:
        # print(row)
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []
    
    open_list.append(start_node)

    while len(open_list) > 0:
        # Get the current node
        current_node = open_list[0]
        current_index = 0
        
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        open_list.pop(current_index)
        closed_list.append(current_node)
#         # print(current_node.position)
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
                # print(path)
            return path[::-1] # Return reversed path

        
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue
            if maze[node_position[0]][node_position[1]] == 1:
                continue
            
            new_node = Node(current_node, node_position)
            # print("New node :",node_position)
            
            children.append(new_node)

            for child in children:
                for closed_child in closed_list:
                    if child == closed_child:
                        continue
                
                child.g = child.parent.g + 1
                # child.h = (end_node.position[0] - node_position[0])**2 + (end_node.position[1] - node_position[1])**2
                # child.h = (end_node.position[0] - node_position[0])**2 + (end_node.position[1] - node_position[1]) ** 2
                child.h = distance.cityblock(node_position, end_node.position)
                child.f = child.g + child.h
            
            for open_node in open_list:
                if open_node == child and open_node.f < child.f:
                    continue
            
            open_list.append(child)

# def main():
# game_folder = path.dirname(__file__)
# img_folder = path.join(game_folder, 'images')
# map_data = []
# with open(path.join(game_folder, 'map.txt'), 'rt') as f:
#     for line in f:
#         map_data.append(line)

# my_maze = []
# map_len = len(map_data[0])
# row_index = 0
# col_index = 0
def maze_transform(maze,map):
    for row, tiles in enumerate(map):
        el_row = []
        for col, tile in enumerate(tiles):
            if tile =='G':
                pass# print("Ghost :",(row,col))
            if tile =='P':
                player_coordinates = (row,col)
                # print("Player :",(row,col))
            if tile == '\n':
                break
            # if (el_row_index == 0 and col_index == 12) or el_row_index == 7 and col_index == 14 :
            #       el_row.append("P")    
            if tile=='.' or tile =='G' or tile == 'P':
                el_row.append(0)    
            else:
                el_row.append(1)
           
        maze.append(el_row)
    return player_coordinates
 
# maze_transform(my_maze,map_data)
# for row in my_maze:
#         print(row)

# for row in my_maze:
#     print(row)

# maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

# start = (9, 13)
# end = (10, 10)


# path = a_star(my_maze, start, end)
# print(path)

