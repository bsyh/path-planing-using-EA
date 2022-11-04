def generate_grid(m,n,fill_element=0):
    '''
    generate a 2-D nested list
    :param m: the number of rows
    :param n: the number of columns
    :param fill_element: the element filled into each spot
    :return: the nested list
    '''
    grid=[]
    for row in range(m):
        grid.append([])
        for column in range(n):
            grid[-1].append(fill_element)
    return grid

def move(position, world, direction):
    '''
    return the position after a move
    :param position: current position
    :param dimension: the dimension of grid world
    :param direction: 0-north, 1-south, 2,west, 3-east
    :return: the position after move
    '''
    row, column = len(world), len(world[0])
    x, y = position
    if direction==0:
        # ensure not moving out of grid-world boundary
        x = max(0,x-1)
    elif direction==1:
        x = min(row-1, x + 1)
    elif direction==2:
        y = max(0, y - 1)
    else:
        y = min(column-1, y + 1)
    new_position = [x, y]
    if world[x][y]:
        return new_position
    return position


def get_reward(position,final_state):
    '''
    this functions defines the reward of grid-world
    :param position: the position of arrival
    :param final_state: goal state
    :return: return the reward of arriving a position
    '''
    x, y = position
    x0, y0 = final_state
    reward = -((x-x0)**2+(y-y0)**2)**0.5
    if position == final_state:
        return 100000
    return reward

def display(table):
    '''
    helper function that displays 2-D nested list
    :param table: 2-D nested list
    :return: None
    '''
    for i in range(len(table)):
        for j in range(len(table[i])):
            print(table[i][j],end='\t')
        print()

def display_path(path,maze,start_state,destination_state):
    '''
    display path in maze

    north ^
    south v
    west <
    east >

    start position "S"
    destination "D"

    :param path: path to be display
    :param maze: grid world
    :param start_state: the position path start at
    :param destination_state: destination position
    :return:
    '''


    m,n=len(maze),len(maze[0])


    display_map = generate_grid(m,n,fill_element=' ')
    for i in range(m):
        for j in range(n):
            if not int(maze[i][j]):
                display_map[i][j] = "·"


    current_position = start_state
    for step in range(len(path)):

        direction = path[step]
        if direction == 0:
            direction_display = "^"
        elif direction == 1:
            direction_display = "v"
        elif direction == 2:
            direction_display = "<"
        else:
            direction_display = ">"
        display_map[current_position[0]][current_position[1]] = direction_display
        current_position = move(current_position, maze, direction)

    display_map[start_state[0]][start_state[1]] = "S"
    display_map[destination_state[0]][destination_state[1]] = "D"
    display(display_map)
