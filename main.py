from pipes import *

if __name__ == "__main__":
    
    sample_grid =   ((0b1000, 0b1001, 0b1011, 0b1010),
                    (0b0011, 0b0101, 0b1110, 0b0111),
                    (0b1011, 0b0001, 0b0010, 0b1000),
                    (0b0110, 0b1100, 0b0010, 0b0010))
    #pipes = show_grid(sample_grid)
    
    print("gurt: yo")
    loaded_pipes = loadFile(select_file())
    grid = Grid(loaded_pipes)
    i=0
    for row in loaded_pipes:
        for val in row:
            i+=1
            if(i==16):
                print(val.whereIsPipe())
                #print(val)
                for ii in (val.checkNeighbors(loaded_pipes)):
                    print(ii)