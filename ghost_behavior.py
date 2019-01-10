from math import sqrt

def pinky_beh(maze, position, dir):
    #dir - direction : if player moving right - +1 if moving left -1
    #position - player position at the moment 
    wall_arr=['C','V','N','B','F','J','M']
    dest = None
    index = 2
    # print("Direction in module:", dir)
    # print("Position in module:",position)
    while dest is None:
        neingh = [(0, index * dir), (-index * dir , 0)]
        for new_position in neingh:
            new_node_r = new_position[0] + position[0]
            new_node_c = new_position[1] + position[1]
            # print("Index:",index)
            # print("Pot position:",(new_position[0] + position[0],new_position[1] + position[1]))
            if len(maze)>new_node_r >= 0 and len(maze[0])>new_node_c >= 0 and maze[new_node_r][new_node_c] != 1 and maze[new_node_r][new_node_c] != 'O' and maze[new_node_r][new_node_c] not in wall_arr: 
                dest = new_position[0] + position[0],new_position[1] + position[1]
        index += 1
        if index > 10:
            break
    return dest

# def corner_choice(ghost_now,corners):
#     closest = corners[0]
#     dist = closest - cor
#     for corner_in_corners:
        

def clyde_beh(g_pos,p_pos):
    if sqrt((g_pos[0] - p_pos[0])**2 + (p_pos[1] - g_pos[1])**2)<3:
            #distance between clyde and player is lesser than 8 , so it is time to run away
        return 0 
    else:
        return 1

def dist(g_pos,p_pos):
    return int(sqrt((g_pos[0] - p_pos[0])**2 + (p_pos[1] - g_pos[1])**2)) 

def inky_beh(maze,position,dir,data_for_inky):
    new_position = pinky_beh(maze,position,dir)
    print("Data for inky",data_for_inky)
    print("New position :",new_position)
    wall_arr=['C','V','N','B','F','J','M']
    new_inky_position = None
    while new_inky_position is None:
        new_node_r = new_position[1] - data_for_inky % (len(maze)-1)
           
        if len(maze)>new_node_r>= 0 and maze[new_position[0]][new_node_r] != 1 and maze[new_position[0]][new_node_r] != 'O' and maze[new_position[0]][new_node_r] not in wall_arr: 
                new_inky_position = new_position[0],new_node_r
        data_for_inky += 1
        
    return new_position
        
