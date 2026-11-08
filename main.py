from pipes import *
import pipes
if __name__ == "__main__":
    
    sample_grid =   ((0b1000, 0b1001, 0b1011, 0b1010),
                    (0b0011, 0b0101, 0b1110, 0b0111),
                    (0b1011, 0b0001, 0b0010, 0b1000),
                    (0b0110, 0b1100, 0b0010, 0b0010))
    pipes.show_grid(sample_grid)
    
    print("gurt: yo")
    print(loadFile("tiles.txt"))