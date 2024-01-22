import random
import time
from copy import copy, deepcopy
from collections import deque


def initialize_grid(grid_size, num_carrot, num_holes):
    grid = [['-' for _ in range(grid_size)] for _ in range(grid_size)]

    rabbit_x, rabbit_y = random.randint(
        0, grid_size-1), random.randint(0, grid_size-1)
    grid[rabbit_x][rabbit_y] = 'r'

    carrots = []
    for _ in range(num_carrot):
        while True:
            x, y = random.randint(
                0, grid_size-1), random.randint(0, grid_size-1)
            if grid[x][y] == '-':
                grid[x][y] = 'c'
                carrots.append((x, y))
                break

    holes = []
    for _ in range(num_holes):
        while True:
            x, y = random.randint(
                0, grid_size-1), random.randint(0, grid_size-1)
            if grid[x][y] == '-':
                grid[x][y] = 'O'
                holes.append((x, y))
                break

    return grid, rabbit_x, rabbit_y, carrots, holes


def display_grid(grid):
    for row in grid:
        print(" ".join(row))


def jump(grid, rabbit_x, rabbit_y):
    isCrossed = False
    grid_size = len(grid)
    new_x = rabbit_x
    new_y = rabbit_y
    if rabbit_x-2 >= 0 and grid[rabbit_x-1][rabbit_y] == 'O':
        new_x = rabbit_x-2
        isCrossed = True
    if rabbit_y-2 >= 0 and grid[rabbit_x][rabbit_y-1] == 'O' and not isCrossed:
        new_y = rabbit_y-2
        isCrossed = True
    if rabbit_x+2 < grid_size and grid[rabbit_x+1][rabbit_y] == 'O' and not isCrossed:
        new_x = rabbit_x+2
        isCrossed = True
    if rabbit_y+2 < grid_size and grid[rabbit_x][rabbit_y+1] == 'O' and not isCrossed:
        new_y = rabbit_y+2
        isCrossed = True
    return (new_x, new_y, isCrossed)


def adjacent_target_cord(grid, rabbit_x, rabbit_y, target):
    adj = [(0, -1), (0, 1), (-1, 0), (1, 0),
           (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dx, dy in adj:
        new_x, new_y = rabbit_x + dx, rabbit_y + dy
        if 0 <= new_x < len(grid) and 0 <= new_y < len(grid) and grid[new_x][new_y] == target:
            return (new_x, new_y)
    return (-1, -1)


class Path:
    def __init__(self, x, y, path):
        self.x = x
        self.y = y
        self.path = path


def bfs(grid, moves, start_x, start_y, goal_x, goal_y):
    visited = set()
    queue = deque([Path(start_x, start_y, [])])

    while queue:
        val = queue.popleft()
        x, y, path = val.x, val.y, val.path
        if abs(x - goal_x) <= 1 and abs(y - goal_y) <= 1:
            # print(path)
            return path

        for dx, dy in moves:
            new_x, new_y = x + dx, y + dy
            if (0 <= new_x < len(grid) and 0 <= new_y < len(grid)) and ((new_x, new_y) not in visited) and (grid[new_x][new_y] != 'c'):
                if grid[new_x][new_y] == 'O':
                    new_x, new_y, isCrossed = jump(grid, x, y)
                    if isCrossed:
                        visited.add((new_x, new_y))
                        queue.append(
                            Path(new_x, new_y, path + [(new_x, new_y)]))
                else:
                    visited.add((new_x, new_y))
                    queue.append(Path(new_x, new_y, path + [(new_x, new_y)]))

    return []


def find_shortest_path_to_win(grid, rabbit_x, rabbit_y, carrots, holes):
    moves = [(0, -1), (0, 1), (-1, 0), (1, 0),
             (-1, -1), (-1, 1), (1, -1), (1, 1)]

    path_to_carrot = []
    path_to_hole = []

    shortest_path_len = float('inf')

    for carrot_x, carrot_y in carrots:
        new_x, new_y = rabbit_x, rabbit_y
        new_path_to_carrot = bfs(
            grid, moves, rabbit_x, rabbit_y, carrot_x, carrot_y)
        for hole_x, hole_y in holes:
            if len(new_path_to_carrot):
                new_x, new_y = new_path_to_carrot[-1]
            new_path_to_hole = bfs(grid, moves, new_x, new_y, hole_x, hole_y)

            total_path_len = len(new_path_to_carrot) + len(new_path_to_hole)
            # print(total_path_len)
            if total_path_len < shortest_path_len:
                # display_grid(grid)
                shortest_path_len = total_path_len
                path_to_carrot = new_path_to_carrot[:]
                path_to_hole = new_path_to_hole[:]

    return (path_to_carrot, path_to_hole)


def simulate(grid, rabbit_x, rabbit_y, path_to_carrot, path_to_hole, user_steps):
    steps = 0
    display_grid(grid)
    print("Next step: \n")
    for x, y in path_to_carrot:
        grid[rabbit_x][rabbit_y] = '-'
        grid[x][y] = 'r'
        rabbit_x, rabbit_y = x, y
        steps += 1
        display_grid(grid)
        print("Next step: \n")
        time.sleep(2)

    temp_x, temp_y = adjacent_target_cord(grid, rabbit_x, rabbit_y, 'c')
    grid[temp_x][temp_y] = '-'
    grid[rabbit_x][rabbit_y] = 'R'
    steps += 1
    display_grid(grid)
    print("Next step: \n")
    time.sleep(2)

    for x, y in path_to_hole:
        grid[rabbit_x][rabbit_y] = '-'
        grid[x][y] = 'R'
        rabbit_x, rabbit_y = x, y
        steps += 1
        display_grid(grid)
        print("Next step: \n")
        time.sleep(2)

    grid[rabbit_x][rabbit_y] = 'r'
    steps += 1
    display_grid(grid)
    time.sleep(2)
    print("Minimum number of steps required: ", steps)
    print("Total number of steps you made: ", user_steps)


# initialize_grid
grid_size = int(input("Enter grid size: "))
num_carrot = int(input("Enter number of carrot: "))
num_holes = int(input("Enter number of holes: "))

grid, rabbit_x, rabbit_y, carrots, holes = initialize_grid(
    grid_size, num_carrot, num_holes)
grid_1 = deepcopy(grid)
rabbit_x_1 = rabbit_x
rabbit_y_1 = rabbit_y
carrot_held = False
isWon = False
user_steps = 0

while True:
    display_grid(grid)
    move = input("Enter move : ")
    user_steps += 1

    dx, dy = 0, 0

    if 'a' in move:
        dy -= 1
    if 's' in move:
        dx += 1
    if 'w' in move:
        dx -= 1
    if 'd' in move:
        dy += 1

    new_x, new_y = rabbit_x + dx, rabbit_y + dy
    if 0 <= new_x < grid_size and 0 <= new_y < grid_size and grid[new_x][new_y] != 'c' and grid[new_x][new_y] != 'O':
        grid[rabbit_x][rabbit_y], grid[new_x][new_y] = '-', 'R' if carrot_held else 'r'
        rabbit_x, rabbit_y = new_x, new_y

    if move == 'p':
        adj = [(0, -1), (0, 1), (-1, 0), (1, 0),
               (-1, -1), (-1, 1), (1, -1), (1, 1)]
        if carrot_held:
            for dx, dy in adj:
                new_x, new_y = rabbit_x + dx, rabbit_y + dy
                if 0 <= new_x < grid_size and 0 <= new_y < grid_size and grid[new_x][new_y] == 'O':
                    carrot_held = False
                    isWon = True
                    grid[rabbit_x][rabbit_y] = 'r'
                    break
        else:
            for dx, dy in adj:
                new_x, new_y = rabbit_x + dx, rabbit_y + dy
                if 0 <= new_x < grid_size and 0 <= new_y < grid_size and grid[new_x][new_y] == 'c':
                    grid[new_x][new_y] = '-'
                    carrot_held = True
                    grid[rabbit_x][rabbit_y] = 'R'
                    break

    elif move == 'q':
        break

    elif move == 'j':
        new_x, new_y, _ = jump(grid, rabbit_x, rabbit_y)
        grid[rabbit_x][rabbit_y], grid[new_x][new_y] = '-', 'R' if carrot_held else 'r'
        rabbit_x, rabbit_y = new_x, new_y

    if isWon:
        display_grid(grid)
        print("Congrats! You won! \n")
        print("Here is an efficient approach: ")

        path_to_carrot, path_to_hole = find_shortest_path_to_win(
            grid_1, rabbit_x_1, rabbit_y_1, carrots, holes)
        simulate(grid_1, rabbit_x_1, rabbit_y_1,
                 path_to_carrot, path_to_hole, user_steps)
        # print(path_to_carrot)
        # print(path_to_hole)
        break
