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



def show_grid(grid, graphics=PIPE_GRAPHICS):
    # Load every tile once, straight from the paths in the dict
    tiles = {mask: plt.imread(path) for mask, path in graphics.items()}

    
    rows = [np.hstack([tiles[frozenbitarray(format(mask, '04b'))] for mask in row])
        for row in grid]
    image = np.vstack(rows)

    plt.imshow(image, interpolation="nearest") 
    plt.axis("off")
    plt.show()

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
    def rotatePipe(self):
        self.pipe = (self.pipe >> 1 | self.pipe << 3) 
        # Perform left shift and wrap around the overflow bits
        #rotates pipe once
    def whereIsPipe(self):
        return (self.row, self.col)
        #output = [x][y]
    def checkNeighbors(self,grid):
        cur_x, cur_y = self.whereIsPipe()[0], self.whereIsPipe()[1]
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
    
        
class Grid:
    def __init__(self):
        pass

    
    def show_grid(grid):
       pass
        

def loadFile(location: str):
    pipes = []
    # https://numpy.org/devdocs/user/absolute_beginners.html
    # 2d array, 7 rows of 7 binary objects
    row = 0
    cur_row = []
    with open(location) as f:
        for line in f:
            if not line.startswith("#"):
                if line == "\n":
                    row += 1
                    pipes.append(cur_row)
                    cur_row = []
                    continue
                pipe = Pipe(line, len(pipes), len(cur_row))
                cur_row.append(pipe)
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
