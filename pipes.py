import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
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
    0b0010: GRAPHICS_DIR / "image1_up.png",     # end cap, opens south
    0b0001: GRAPHICS_DIR / "image1_right.png",  # end cap, opens west
    0b1000: GRAPHICS_DIR / "image1_down.png",   # end cap, opens north
    0b0100: GRAPHICS_DIR / "image1_left.png",   # end cap, opens east
    0b1010: GRAPHICS_DIR / "image2_up.png",     # straight vertical
    0b0101: GRAPHICS_DIR / "image2_right.png",  # straight horizontal
    0b1100: GRAPHICS_DIR / "image3_up.png",     # elbow N+E
    0b0110: GRAPHICS_DIR / "image3_right.png",  # elbow E+S
    0b0011: GRAPHICS_DIR / "image3_down.png",   # elbow S+W
    0b1001: GRAPHICS_DIR / "image3_left.png",   # elbow W+N
    0b1110: GRAPHICS_DIR / "image4_up.png",     # T  N+E+S
    0b0111: GRAPHICS_DIR / "image4_right.png",  # T  E+S+W
    0b1011: GRAPHICS_DIR / "image4_down.png",   # T  S+W+N
    0b1101: GRAPHICS_DIR / "image4_left.png",   # T  W+N+E
}



def show_grid(grid, graphics=PIPE_GRAPHICS):
    # Load every tile once, straight from the paths in the dict
    tiles = {mask: plt.imread(path) for mask, path in graphics.items()}

    # Stitch each row side by side, then stack the rows top to bottom
    rows = [np.hstack([tiles[mask] for mask in row]) for row in grid]
    image = np.vstack(rows)

    plt.imshow(image, interpolation="nearest")  # "nearest" keeps pixels crisp
    plt.axis("off")
    plt.show()


class Pipe:
    def __init__(self,pipe):
        # u = up r = right d = down l = left
        # https://www.geeksforgeeks.org/python/working-with-binary-data-in-python/
        self.u, self.r, self.d, self.l = 0b1000,0b0100,0b0010,0b0001
        self.pipe = bin(int(pipe))
        self.opposite_directions = {self.u: self.d, self.r: self.l, self.d: self.u, self.l: self.r}
        # for each tile check for matching opposite direcitons (if they have them), if they connect NOT a leak
        # if they dont connect assume there's a leak. rotate until all opposite directions map
    def rotatePipe(self):
        #rotates pipe once
        return (self.pipe << 1)
    def whereIsPipe(self,grid):
        return np.argwhere(grid == self.pipe)
        #output = [x][y]
    def checkOpposite(self,grid):
        #pipe_location = whereIsPipe(grid)
        for _ in range(4):
            pass   
        pass
    
        
class Grid:
    def __init__(self):
        pass

    
    def show_grid(grid):
       pass
        

def loadFile(location: str):
    pipes = [[]]
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
                pipe = Pipe(line)
                cur_row.append(pipe)

    return pipes