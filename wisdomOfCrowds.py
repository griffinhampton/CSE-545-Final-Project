from collections import Counter
import copy
from pipes import Grid, Pipe

class WisdomOfCrowds:
    def __init__(self, ga_runner, runs=10, agreement_threshold=0.75):
        self.ga_runner = ga_runner
        self.runs = runs
        self.threshold = agreement_threshold
        
    def collect_crowd(self):
        crowd_solutions = []
        for i in range(self.runs):
            best_sol = self.ga_runner()
            crowd_solutions.append(best_sol)
        return crowd_solutions
    
    def extract_rotations(self, grid_pipes):
        return [[str(pipe.pipe.to01()) for pipe in row] for row in grid_pipes]
    
    def aggregate_consensus(self, crowd_solutions):
        # Count the frequency of each solution
        rows = len(crowd_solutions[0])
        cols = len(crowd_solutions[0][0])
        
        consensus_grid = [[None for _ in range(cols)] for _ in range(rows)]
        fixed_mask = [[False for _ in range(cols)] for _ in range(rows)]
        stats = []
        
        for r in range(rows):
            for c in range(cols):
                votes = Counter(sol[r][c] for sol in crowd_solutions)
                most_common_pipe, count = votes.most_common(1)[0]
                agreement_ratio = count / self.runs
                
                consensus_grid[r][c] = most_common_pipe
                if agreement_ratio >= self.threshold:
                    fixed_mask[r][c] = True
                    
                stats.append(((r, c), most_common_pipe, agreement_ratio))
                
        return consensus_grid, fixed_mask, stats
    
    def build_grid_from_bitstrings(self, bitstring_matrix):
        new_pipes = []
        for r, row in enumerate(bitstring_matrix):
            cur_row = []
            for c, bit_str in enumerate(row):
                cur_row.append(Pipe(bit_str, r, c))
            new_pipes.append(cur_row)
        return Grid(new_pipes)