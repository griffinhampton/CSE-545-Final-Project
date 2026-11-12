import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from bitarray import bitarray,frozenbitarray
"""
pipes need:
    directions it's opened (D = {n,e,s,w} )
    + shapes of each pipe (4 possible options, -, L, T, +)

options for pipes:
    URDL (1, 0, 0, 1)
    U = 0 R = 1 D = 2 L = 3

(1, 0, 1, 0) = |
(0, 1, 0, 1) = -

(1, 0, 1, 0) = |
(1, 1, 0, 0) = L


in order when making this
    1. shuffle solved map for each GA running
    2. run GA for each shuffled board:
        randomly reshuffle every tile (except the ones inherited by the parent)
        iterate through shuffled tiles finding every leak 


    for tile in grid:
        for side in tile:
            if side = 1 and adjacent tile's opposite side = 1:
                connection/no leak

"""

GRAPHICS_DIR = Path(__file__).parent / "pipe_graphics"

PIPE_GRAPHICS = {
    frozenbitarray('0010'): GRAPHICS_DIR / "image1_up.png",     # end cap, opens south
    frozenbitarray('0001'): GRAPHICS_DIR / "image1_right.png",  # end cap, opens west
    frozenbitarray('1000'): GRAPHICS_DIR / "image1_down.png",   # end cap, opens north
    frozenbitarray('0100'): GRAPHICS_DIR / "image1_left.png",   # end cap, opens east
    frozenbitarray('1010'): GRAPHICS_DIR / "image2_up.png",     # straight vertical
    frozenbitarray('0101'): GRAPHICS_DIR / "image2_right.png",  # straight horizontal
    frozenbitarray('1100'): GRAPHICS_DIR / "image3_up.png",     # elbow N+E
    frozenbitarray('0110'): GRAPHICS_DIR / "image3_right.png",  # elbow E+S
    frozenbitarray('0011'): GRAPHICS_DIR / "image3_down.png",   # elbow S+W
    frozenbitarray('1001'): GRAPHICS_DIR / "image3_left.png",   # elbow W+N
    frozenbitarray('1110'): GRAPHICS_DIR / "image4_up.png",     # T  N+E+S
    frozenbitarray('0111'): GRAPHICS_DIR / "image4_right.png",  # T  E+S+W
    frozenbitarray('1011'): GRAPHICS_DIR / "image4_down.png",   # T  S+W+N
    frozenbitarray('1101'): GRAPHICS_DIR / "image4_left.png",   # T  W+N+E
}



_TILE_CACHE = {}

def show_grid(grid, graphics=PIPE_GRAPHICS, pause_time=0.05, title=None):
    global _TILE_CACHE
    if not _TILE_CACHE:
        _TILE_CACHE = {mask: plt.imread(path) for mask, path in graphics.items()}

    # Support either a Grid instance or a 2D list of Pipes/bitarrays
    pipe_rows = grid.pipes if hasattr(grid, "pipes") else grid
    rows = []
    for row in pipe_rows:
        row_imgs = []
        for cell in row:
            mask = cell.pipe if hasattr(cell, "pipe") else cell
            row_imgs.append(_TILE_CACHE[mask])
        rows.append(np.hstack(row_imgs))

    image = np.vstack(rows)

    plt.clf()
    plt.imshow(image, interpolation="nearest")
    if title:
        plt.title(title)
    plt.axis("off")
    plt.draw()
    plt.pause(pause_time)

# ALSO - BITARRAYS CANNOT BE HASHED SO PIPE_GRAPHICS[pipe.pipe] WILL CRASH
# you MUST turn it into an int int(pipe.pipe.to01(), 2) to match it w current dictionary
class Pipe:
    def __init__(self,pipe, row, col):
        self.row = row
        self.col = col
        # u = up r = right d = down l = left
        # https://www.geeksforgeeks.org/python/working-with-binary-data-in-python/
        self.u, self.r, self.d, self.l = '1000','0100','0010','0001'
        self.pipe = frozenbitarray(pipe) 
        self.opposite_directions = {self.u: self.d, self.r: self.l, self.d: self.u, self.l: self.r}
        # for each tile check for matching opposite direcitons (if they have them), if they connect NOT a leak
        # if they dont connect assume there's a leak. rotate until all opposite directions map
    def __str__(self):
        return self.pipe.to01()
    def rotate_pipe(self):
        self.pipe = (self.pipe >> 1 | self.pipe << 3) 
        # Perform left shift and wrap around the overflow bits
        #rotates pipe once
    def where_is_pipe(self):
        return (self.row, self.col)
        #output = [x][y]
    def check_neighbors(self,grid):
        cur_x, cur_y = self.where_is_pipe()[0], self.where_is_pipe()[1]
        #pipe_location = whereIsPipe(grid)
        neighborPipes = []
        max_size=len(grid)
        for r, c in [(-1,0),(0,1), (1,0), (0,-1)]:
            row = cur_x + r
            col = cur_y + c
            if (not((row < 0 or col < 0 ) or (row >= max_size or col >= max_size))):
                neighborPipes.append(grid[row][col])
            else:
                neighborPipes.append(None)
        return neighborPipes
        #up, right, down, left
    def check_leaks(self,grid):
        leaks = 0
        neighbors = self.check_neighbors(grid)
        for i in range(4): #checking each side
            if self.pipe[i]: # iterates thru each binary value, 1 or 0 for each (open or closed)
                neighbor = neighbors[i] # works bc if pipe is open on a side, the neighbor[i] would check the pipe on that side
                opposite = (i + 2) % 4 # reverse logic of neighbor
                if neighbor is None or not neighbor.pipe[opposite]:
                    #if there is no pipe there or there is one but it's closed on the side facing the other pipe
                    #then the opening leads nowhere, making a leak
                    leaks +=1
        return leaks
    def connected_neighbors(self,grid):
        connected = []
        neighbors = self.check_neighbors(grid)
        for i in range(4): #checking each side
            if self.pipe[i]: # iterates thru each binary value, 1 or 0 for each (open or closed)
                neighbor = neighbors[i] # works bc if pipe is open on a side, the neighbor[i] would check the pipe on that side
                opposite = (i + 2) % 4 # reverse logic of neighbor
                if self.pipe[i] and neighbor is not None and neighbor.pipe[opposite]:
                    # if there is a pipe there or there is one and it's connected and facing the other pipe
                    connected.append(neighbor)
        return connected
        
class Grid:
    def __init__(self, pipes):
        self.pipes = pipes

    def show_grid(grid):
        pass

    def check_grid(self):
        leaksForAllPipes = [] # Will contain lists of [[0, 1], [1, 0]] meaning tile 0 has 1 leak, tile 1 has 0 leaks, etc
        islandNumber = {} 
        #the idea for islands is that each pipe is assumed to be an island, whenever proven false the island status
        #moves to the next pipe, if it doesnt move assume it's an island 
        i = 0
        for row in self.pipes:
            for pipe in row:
                leaksForAllPipes.append([i, pipe.check_leaks(self.pipes)])
                islandNumber[pipe] = i # every pipe starts its own number
                for neighbor in pipe.connected_neighbors(self.pipes):
                    if neighbor in islandNumber and islandNumber[neighbor] !=i:
                        # only do anything if loop reached this before (if neighbor in islandNumber)
                        # AND the neighbor is on a different island than the current pipe (where 1 is the pipes number)
                        temp = islandNumber[neighbor]
                        for pp in islandNumber:
                            # move everything from old island here, continuing it (eventually finding the end)
                            if islandNumber[pp] == temp:
                                islandNumber[pp] = i
                i += 1
        islands = len(set(islandNumber.values()))
        # we can score the islands however we want
        return leaksForAllPipes, islands
        

def loadFile(location: str):
    pipes = []
    # https://numpy.org/devdocs/user/absolute_beginners.html
    # 2d array, 7 rows of 7 binary objects
    cur_row = []
    with open(location) as f:
        for line in f:
            if not line.startswith("#"):
                stripped = line.strip()
                if stripped == "":
                    if cur_row:
                        pipes.append(cur_row)
                        cur_row = []
                    continue
                pipe = Pipe(line, len(pipes), len(cur_row))
                cur_row.append(pipe)
        if cur_row:
            pipes.append(cur_row)
    return pipes

BASE_DIR = Path(__file__).resolve().parent

def select_file():
    files = sorted(BASE_DIR.glob("*.txt"))
    if not files:
        print("No .txt files found in the current directory.")
        return None
    print("\nSelect a txt file:")
    for index, file_path in enumerate(files, start=1):
        print(f"  {index}. {file_path.name}")
    while True:
        selection = input("File number: ").strip()
        if selection.isdigit() and 1 <= int(selection) <= len(files):
            return files[int(selection) - 1]
        print("Please enter a valid file number.")
