def maze_transform(maze,map):
    for row, tiles in enumerate(map):
        el_row = []
        for col, tile in enumerate(tiles):
            if tile == '\n':
                break
            elif tile =='G':
                el_row.append('G')
            #     # pass# print("Ghost :",(row,col))
            elif tile =='D':
                el_row.append('D')
            elif tile =='p':
                #pinky
                el_row.append('p')
            elif tile =='i':
                #inky
                el_row.append('i')
            elif tile =='c':
                #clyde
                el_row.append('c')
            elif tile =='O':
                #empty tile inside of block
                el_row.append('O')

            elif tile =='P':
                el_row.append('P')
                player_coordinates = (row,col)
            elif tile == ' ':
                el_row.append(2)
            elif tile == 'H': #ghost_house
                el_row.append('H')
            elif tile == 'C':
                el_row.append('C')
            elif tile == 'V':
                el_row.append('V')
            elif tile == 'N':
                el_row.append('N')
            elif tile == 'B':
                el_row.append('B')
            elif tile == 'F':
                el_row.append('F')
            #     # print("Player :",(row,col))
            elif tile == 'J':
                el_row.append('J')
            elif tile == 'M':
                el_row.append('M')
           
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
 


def ghost_house_area(maze , ghost_house):
    ghost_house_area = [ghost_house]
    index = 0
    output = [ghost_house]
    wall_arr=['C','V','N','B','F','J','M','O','D',1]
    neingh = [(0, -1), (0, 1), (-1, 0),(1, 0)]
    node = maze[ghost_house_area[0][0]][ghost_house_area[0][1]]
    while index < len(maze[0]) * 2:
            # print(frontier)
            print(ghost_house_area)
            current = ghost_house_area[0]
            ghost_house_area.pop(0)
            for new_position in [(0, -1), (0, 1), (-1, 0),(1, 0)]:
                new_node_r = new_position[0] + current[0]
                new_node_c = new_position[1] + current[1]
                if (new_node_r,new_node_c) not in ghost_house_area and  maze[new_node_r][new_node_c] not in wall_arr: 
                    new_node = new_position[0] + current[0],new_position[1] + current[1]
                    # print(current,"------------>",new_node)
                    ghost_house_area.append(new_node)         
                output.append(new_node)
                index += 1
       
    output.append(ghost_house)
    return output
        

def breadth_search(maze,start,end, runnig = None):
    try:
        wall_arr=['C','V','N','B','F','J','M']
        if runnig:
            print("running")
            wall_arr.append('P')
        frontier = [start]
        visited = {start:None}
        while frontier:
            # print(frontier)
            current = frontier[0]
            frontier.pop(0)
            for new_position in [(0, -1), (0, 1), (-1, 0),(1, 0)]:
                new_node_r = new_position[0] + current[0]
                new_node_c = new_position[1] + current[1]
                
                if len(maze)>new_node_r >= 0 and len(maze[0])>new_node_c >= 0 and (new_node_r,new_node_c) not in visited and maze[new_node_r][new_node_c] != 1 and maze[new_node_r][new_node_c] != 'O' and maze[new_node_r][new_node_c] not in wall_arr: 
                    new_node = new_position[0] + current[0],new_position[1] + current[1]
                    # print(current,"------------>",new_node)
                    visited[new_node] = current
                    frontier.append(new_node)
                    if new_node == end :
                        break
        # print(visited)
        current = end
        path = []
        wall_arr.pop()
        while current != None:
                path.append(current)
                current = visited[current]
        
        return path[::-1]
    except KeyError:
        print("Error")



    