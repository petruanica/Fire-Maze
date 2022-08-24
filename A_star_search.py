import os

from colors import color_text
from util import Cell, CellList


def solve(maze, start, goals):
    cells = CellList(maze)
    cells.add(Cell(state=start, value=cell_value(goals, start, 0), steps=0, parent=None))
    explored = set()
    while True:
        if cells.empty():
            break
        current = cells.remove()
        explored.add(current.state)
        for cell in actions(maze, current.state):
            if cell in explored or cells.contains_cell(cell):
                continue
            if cell in goals:
                path = [cell]
                while current.parent is not None:
                    path.append(current.state)
                    current = current.parent
                path.reverse()
                # print_solution(maze, path, start, goal)
                return path
            cells.add(Cell(state=cell, value=cell_value(goals, cell, current.steps + 1), steps=current.steps + 1, parent=current))
    return None


def actions(maze, current):
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    available_actions = []
    for d in directions:
        temp = (current[0] + d[0], current[1] + d[1])
        if temp[0] in range(len(maze)) and temp[1] in range(len(maze[0])) and maze[temp[0]][temp[1]] < 0.6:
            available_actions.append(temp)
    return available_actions


def cell_value(goals, cell, steps):
    return steps + min(abs(goal[0] - cell[0]) + abs(goal[1] - cell[1]) for goal in goals)


def print_solution(maze, path, start, goals):
    os.system('color')
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if (i, j) == start:
                print(color_text("A", color="green"), end="")
            elif (i, j) in goals:
                print(color_text("B", color="green" if (i, j) in path else "blue"), end="")
            elif (i, j) in path:
                print(color_text("*", color="green"), end="")
            elif maze[i][j] == 1:
                print("#", end="")
            elif 0.1 <= maze[i][j] < 0.3:
                print(color_text("!", color="green", style="bold"), end="")
            elif 0.3 <= maze[i][j] < 0.6:
                print(color_text("!", color="yellow", style="bold"), end="")
            elif 0.6 <= maze[i][j] < 1:
                print(color_text("!", color="red", style="bold"), end="")
            else:
                print("_", end="")
        print()
    print()
