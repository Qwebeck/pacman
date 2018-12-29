def maze_transform(maze,map):
    for row, tiles in enumerate(map):
        el_row = []
        for col, tile in enumerate(tiles):
            if tile == '\n':
                break
            elif tile =='G':
                el_row.append('G')
            #     # pass# print("Ghost :",(row,col))
            elif tile =='p':
                #pinky
                el_row.append('p')
            elif tile =='i':
                #inky
                el_row.append('i')
            elif tile =='c':
                #clyde
                el_row.append('c')
            elif tile =='P':
                el_row.append('P')
                player_coordinates = (row,col)
            elif tile == ' ':
                el_row.append(2)
            elif tile == 'H': #ghost_house
                el_row.append('H')

            #     # print("Player :",(row,col))
           
            elif tile == '3':
                el_row.append(3)
            # if (el_row_index == 0 and col_index == 12) or el_row_index == 7 and col_index == 14 :
            #       el_row.append("P")    
            elif tile=='.' or tile == ' ':
                el_row.append(0)    
            else:
                el_row.append(1)
           
        maze.append(el_row)
    return player_coordinates
 



def breadth_search(maze,start,end):

    
    frontier = [start]
    visited = {start:None}
    while frontier:
        # print(frontier)
        current = frontier[0]
        frontier.pop(0)
        for new_position in [(0, -1), (0, 1), (-1, 0),(1, 0)]:
            new_node_r = new_position[0] + current[0]
            new_node_c = new_position[1] + current[1]
            if len(maze)>new_node_r >= 0 and len(maze[0])>new_node_c >= 0 and (new_node_r,new_node_c) not in visited and maze[new_node_r][new_node_c] != 1: 
                new_node = new_position[0] + current[0],new_position[1] + current[1]
                # print(current,"------------>",new_node)
                visited[new_node] = current
                frontier.append(new_node)
                if new_node == end :
                    break
    # print(visited)
    current = end
    path = []
    while current != None:
        path.append(current)
        current = visited[current]
    return path[::-1]


    