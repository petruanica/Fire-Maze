class Cell:
    def __init__(self, state, value, steps, parent):
        self.state = state
        self.value = value
        self.steps = steps
        self.parent = parent


class CellList:
    def __init__(self, maze):
        self.cells = []
        self.maze = maze

    def add(self, cell):
        self.cells.append(cell)

    def empty(self):
        return len(self.cells) == 0

    def contains_cell(self, cell):
        return any(cell.state == cell for cell in self.cells)

    def remove(self):
        if self.empty():
            raise Exception("empty list")
        else:
            cell_to_remove = min(self.cells, key=lambda cell: (cell.value, self.maze[cell.state[0]][cell.state[1]]))
            self.cells.remove(cell_to_remove)
            return cell_to_remove
