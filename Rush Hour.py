"""from dataclasses import dataclass"""
import copy
from typing import List, Optional, Tuple

SIZE = 6

def main():
    #gets the information for the puzzle into a board variable
    filename = "puzzle.txt"
    board = read_file(filename)
    print_grid(board.grid)
    print()

    #history = []
    #solution_path, b = solve_recur(board, history)

    solved_board = solve_iter(board)
    solution_path = board_to_path(solved_board)
    if solution_path == None:
        print("no solution found")
        return
    #solution_path = shorten_path(solution_path)
    print_path(solution_path)

def solve_recur(board: "Board", history: List["Board"]) -> Tuple[List[List[str]], bool]:
    """ Solves the curent board state recursively (if possible)
    and returns a list of grids in the order in which they appear
    in the solution path as well as a solved boolean. """
    if board.grid in history:
        path = []
        return path, False
    else:
        history.append(board.grid)
    if is_solved(board.grid):
        path = []
        path.insert(0, board.grid)
        return path, True
    
    neighbors = get_neighbors(board)
    for n in neighbors:
        path, solved = solve_recur(n, history)
        if solved:
            path.insert(0, board.grid)
            return path, True

    path = []
    return path, False

def solve_iter(board: "Board") -> Optional["Board"]:
    """ Solves the curent board state iteratively (if possible)
    and sets the parent of each board in the solution path.
    It returns the final solved board state or None if no solution. """
    #all previously visited board states
    history: List[Board] = []
    #todo is a to-check queue
    todo = [board]
    while todo:
        b = todo.pop(0)
        if b.grid not in history:
            history.append(b.grid)
            for n in get_neighbors(b):
                if n.grid in history:
                    continue
                n.parent = b
                if is_solved(n.grid):
                    return n
                todo.append(n)
    return None

class Car:
    """ A car represents the placement and orentation of a single car in the game. """
    id = ""
    length = 0
    row = 0
    col = 0
    horizontal = False

    def __init__(self, id, length, row, col, horizontal):
        self.id = str(id)
        self.length = int(length)
        self.row = int(row)
        self.col = int(col)
        self.horizontal = bool(horizontal)

class Board:
    """ A board represents the state of a board and consists of
    a list of car objects, a grid (2D array of char),
    and the parent of the board (used in solve_iter to find path). """
    grid = [["0" for i in range(SIZE)] for j in range(SIZE)]
    cars = []
    parent = None
    def __init_(self):
        self.grid = [["0" for i in range(SIZE)] for j in range(SIZE)]
        self.cars = []

def is_solved(grid: List[List[str]]):
    """ Checks if the grid of a board is in a solved state. """
    if grid[2][5] == "x":
        return True
    else:
        return False

def get_neighbors(board: Board) -> List[Board]:
    """ Gets and returns all neighbors of a current Board in a list.
    A neighbor is a board state that is one move away (1 car in one direction for 1 tile)
    from the current board state. """
    #does not include history
    neighbors = []
    for ii, car in enumerate(board.cars):
        if car.horizontal:
            #right
            if car.col + car.length < SIZE:
                if board.grid[car.row][car.col + car.length] == "0":
                    new_board = Board()
                    new_board.grid = copy.deepcopy(board.grid)
                    new_board.cars = copy.deepcopy(board.cars)
                    new_car = new_board.cars[ii]
                    new_board.grid[new_car.row][new_car.col + new_car.length] = new_car.id
                    new_board.grid[new_car.row][new_car.col] = "0"
                    new_car.col += 1
                    neighbors.append(new_board)
            #left
            if car.col - 1 >= 0:
                if board.grid[car.row][car.col - 1] == "0":
                    board.grid[car.row][car.col - 1] = car.id
                    board.grid[car.row][car.col + car.length - 1] = "0"
                    car.col -= 1
                    new_board = Board()
                    new_board.grid = copy.deepcopy(board.grid)
                    new_board.cars = copy.deepcopy(board.cars)
                    neighbors.append(new_board)
                    car.col += 1
                    board.grid[car.row][car.col - 1] = "0"
                    board.grid[car.row][car.col + car.length - 1] = car.id
        else:
            #down
            if car.row + car.length < SIZE:
                if board.grid[car.row + car.length][car.col] == "0":
                    board.grid[car.row + car.length][car.col] = car.id
                    board.grid[car.row][car.col] = "0"
                    car.row += 1
                    new_board = Board()
                    new_board.grid = copy.deepcopy(board.grid)
                    new_board.cars = copy.deepcopy(board.cars)
                    neighbors.append(new_board)
                    car.row -= 1
                    board.grid[car.row + car.length][car.col] = "0"
                    board.grid[car.row][car.col] = car.id
            #up
            if car.row-1 >= 0:
                if board.grid[car.row - 1][car.col] == "0":
                    board.grid[car.row - 1][car.col] = car.id
                    board.grid[car.row + car.length - 1][car.col] = "0"
                    car.row -= 1
                    new_board = Board()
                    new_board.grid = copy.deepcopy(board.grid)
                    new_board.cars = copy.deepcopy(board.cars)
                    neighbors.append(new_board)
                    car.row += 1
                    board.grid[car.row - 1][car.col] = "0"
                    board.grid[car.row + car.length - 1][car.col] = car.id
    return neighbors

def cars_to_grid(board: Board):
    """ Turns the list of cars within a board to a grid
    and reassigns the board's grid to that. """
    #assumes list of cars is correct
    for car in board.cars:
        if car.horizontal:
            for i in range(0, car.length):
                board.grid[car.row][car.col+i] = car.id
        else:
            for i in range(0, car.length):
                board.grid[car.row+i][car.col] = car.id

def grid_to_cars(board: Board):
    """ Turns the grid within a board to a list of cars
    and reassigns the board's list of cars to that. """
    # assumes grid is correct
    grid = board.grid
    symbols = ["0"]
    cars = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            #if new symbol, check for horizantal or vertical, then length
            sym = grid[i][j]
            if sym not in symbols:
                symbols.append(sym)
                is_horizontal = j + 1 <= SIZE - 1 and grid[i][j+1] == sym
                is_vertical = i + 1 <= SIZE - 1 and grid[i+1][j] == sym
                if is_horizontal:
                    n = 2
                    while j + n <= SIZE - 1 and grid[i][j+n] == sym:
                        n += 1
                    cars.append(Car(sym, n, i, j, True))
                elif is_vertical:
                    n = 2
                    while i + n <= SIZE - 1 and grid[i+n][j] == sym:
                        n += 1
                    cars.append(Car(sym, n, i, j, False))
                else:
                    print("invalid board")
    board.cars = cars

def board_to_path(solved_state: Board) -> Optional[List[List[List[str]]]]:
    """ Uses the solved board's parents to constructed the list of grids
    in the original board's solution path. """
    if solved_state:
        solution_path = []
        solution_path.append(solved_state.grid)
        while solved_state.parent is not None:
            solution_path.append(solved_state.parent.grid)
            solved_state = solved_state.parent
        solution_path.reverse()
        return solution_path
    else:
        return None

def shorten_path(path: List[List[List[str]]]) -> List[List[List[str]]]:
    """ An algorithm which striclty decreases the amount of states in
    a boards solution path by identifying if a state further along in the path
    can be reached by one move from the current state. This proccess is repeated
    with all states in the path with the intent to shorten the overall path.
    It works with DFS algorithms and BFS algorithms but only can shorten DFS found paths.
    It takes a list of grids and returns a list of grids. """
    #path must not be None
    shortened_path = [path[0]]
    #while last state in shortened path is not solved state, find next state to add to shortened_path
    while shortened_path[len(shortened_path)-1] != path[len(path)-1]:
        cur_state = shortened_path[len(shortened_path)-1]
        #start checking for one-move-off state at the back of path going to the front
        cur_next_i = len(path) - 1
        while True:
            dif_count = 0
            for row in range(len(cur_state)):
                for col in range(len(cur_state[row])):
                    if cur_state[row][col] != path[cur_next_i][row][col]:
                        dif_count += 1
                        if dif_count > 2:
                            break
                    if dif_count > 2:
                        break
            if dif_count == 2:
                shortened_path.append(path[cur_next_i])
                break
            else:
                cur_next_i -= 1
    return shortened_path

def print_grid(grid: List[List[str]]):
    """ Utility function to print the grid of a board. """
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            print(grid[i][j] + " ", end="")
        print()      

def print_path(path: List[List[List[str]]]):
    """ Utility function to print a list of grids in a path. """
    for i in range(len(path)):
        print(str(i + 1) + ":")
        print_grid(path[i])

def read_file(filename: str) -> Board:
    """ Utility function to read a file which contains a grid
    and puts the information into a board to be returned. """
    b = Board()
    with open(filename) as f:
        for i in range(SIZE):
            line = f.readline()
            j_count = 0
            for j in range(len(line)):
                if line[j] == " " or line[j] == "\n":
                    continue
                else:
                    b.grid[i][j_count] = line[j]
                    j_count += 1
    grid_to_cars(b)
    return b

if __name__=="__main__":
    main()
