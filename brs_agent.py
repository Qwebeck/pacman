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


    