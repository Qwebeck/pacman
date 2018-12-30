maze_3 = [
    [0, 1, 0, 1, 0, 0 ,0],
    [0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 0],
]

def pinky_beh(maze, position, dir):
    #dir - direction : if player moving right - +1 if moving left -1
    dest = None
    print("Direction in module:", dir)
    print("Position in module:",position)
    index = 2
    while dest is None:
        neingh = [(0, index * dir), (index * dir , 0)]
        for new_position in neingh:
            new_node_r = new_position[0] + position[0]
            new_node_c = new_position[1] + position[1]
            if len(maze)>new_node_r >= 0 and len(maze[0])>new_node_c >= 0 and maze[new_node_r][new_node_c] != 1 and maze[new_node_r][new_node_c] != 'O': 
                dest = new_position[0] + position[0],new_position[1] + position[1]
        index += 1
    return dest


dest = pinky_beh(maze_3,(2,3),1)
print("Destination: ",dest)

                # print(position,"------------>",new_node)

 